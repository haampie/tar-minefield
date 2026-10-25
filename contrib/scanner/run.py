"""Download a sample of tarballs and scan them.

    python -I contrib/scanner/run.py sample LIST N SEED > SAMPLE
    python -I contrib/scanner/run.py fraction LIST P SEED > SAMPLE
    python -I contrib/scanner/run.py scan SAMPLE OUT [--untar PATH] [--jobs N] [--reuse FILE]...
        [--cache DIR [--cache-size GB]]

`sample` takes the output of spack_list.py and picks N/2 latest versions of distinct packages,
and N/2 older versions of other distinct packages, in an order that is random but determined by
SEED and the names of packages and checksums of tarballs.

`fraction` takes every tarball whose rank, by SEED and its sha256, is in the lowest fraction P of
all ranks: a sample of about P of the list. Whether a tarball is in it does not depend on the
rest of the list, so a list can be sampled while it is made, and the sample with a larger P
contains the one with a smaller P: a sample can be extended without scanning anything again.
It is in the order of rank, in which `scan` starts downloads, so the tarballs scanned first of a
sample with a large P are the sample with a smaller P: an interrupted scan is a sample too, but
for the few downloads that were under way.

`scan` downloads each tarball from the first of its `urls` that works, scans it while it downloads,
checks its sha256, and appends a JSON line to OUT. A tarball listed with a `member`, as a gem is
with `data.tar.gz`, is an archive of the tarball: its sha256 is checked, and the member is scanned
and extracted, with the features of the outer archive in `member_of`. Tarballs are not written to
disk unless --cache is given, so tarballs of any size are scanned. Tarballs that are already in OUT
are skipped, so an interrupted run can continue. Every line records the version of the scanner, and
of untar, as the start of the sha256 of their source.

With --reuse FILE (repeatable), tarballs that FILE has results for, from the same versions of
the scanner and untar, are not downloaded: their results are copied. So ecosystems that share
tarballs are each sampled in full, while every tarball is downloaded once.

With --untar, each tarball is also extracted by untar from PATH, in a child process that reads
the decompressed archive from a pipe, and its error recorded. If untar runs out of disk space,
that is recorded apart from its errors, and --reuse does not copy it: remove those lines from
OUT and run again, with more space, to extract them.

With --cache DIR, downloads are also kept in DIR, by sha256, up to --cache-size GB (50 by
default): the least recently used are removed first, and tarballs over a tenth of that are not
kept. Tarballs in DIR are scanned from there, so a scan with a new version of the scanner or
untar does not download them again.
"""

import concurrent.futures
import hashlib
import http.client
import io
import json
import lzma
import multiprocessing
import os
import subprocess
import shutil
import sys
import tarfile
import tempfile
import time
import traceback
import urllib.request
import zlib

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tarscan  # noqa: E402

SCANNER = hashlib.sha256(open(tarscan.__file__, "rb").read()).hexdigest()[:12]
# Results of a scan, as opposed to the fields of the list entry of a tarball
SCAN_FIELDS = (
    "bytes",
    "members",
    "kinds",
    "features",
    "examples",
    "fingerprint",
    "mtime",
    "error",
    "compression",
    "compression_error",
    "untar_error",
    "untar_skipped",
    "scanner",
    "untar",
)
USER_AGENT = "tar-minefield-scanner (+https://github.com/haampie/tar-minefield)"


def rank(seed, key):
    """A random but stable order: the order of most keys does not change when others are added
    or removed, so samples of later package lists overlap with earlier ones."""
    return hashlib.sha256(f"{seed}:{key}".encode()).hexdigest()


def fetch(url, accept="*/*"):
    """The body at url, tried again on errors."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(request, timeout=60) as r:
                return r.read()
        except (OSError, http.client.HTTPException):
            if attempt == 4:
                raise


def list_ranked(names, tarballs, n, seed):
    """Print the tarballs of packages, as JSON lines, by the function tarballs of a package name, in
    the order of the rank of packages by seed: only as many as `sample` takes n from, n/2 packages
    with a latest version and n/2 others with an older one. As the rank of a package does not
    depend on the others, the sample of this list is the sample of a list of all packages."""
    names = sorted(names, key=lambda p: rank(seed, p))
    latest, older = 0, 0
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        # in batches, in order, so that the list stops where the sample does
        for start in range(0, len(names), 400):
            for files in pool.map(tarballs, names[start:start + 400]):
                if latest < n // 2:
                    latest += any(f["latest"] for f in files)
                elif older < n - n // 2:
                    older += any(not f["latest"] for f in files)
                else:
                    continue
                for f in files:
                    print(json.dumps(f))
            print(f"{start + 400} packages: {latest} latest, {older} older", file=sys.stderr)
            if latest >= n // 2 and older >= n - n // 2:
                break


def sample(path, n, seed):
    seen = set()
    by_package = {}
    for line in open(path):
        t = json.loads(line)
        if t["sha256"] in seen:
            continue
        seen.add(t["sha256"])
        by_package.setdefault(t["package"], []).append(t)
    packages = sorted(by_package, key=lambda p: rank(seed, p))
    latest = [p for p in packages if any(t.get("latest") for t in by_package[p])][: n // 2]
    taken = set(latest)
    older = [
        p for p in packages if p not in taken and any(not t.get("latest") for t in by_package[p])
    ][: n - len(latest)]
    for p in latest:
        print(json.dumps(next(t for t in by_package[p] if t.get("latest"))))
    for p in older:
        versions = [t for t in by_package[p] if not t.get("latest")]
        print(json.dumps(min(versions, key=lambda t: rank(seed, t["sha256"]))))


def fraction(path, p, seed):
    taken = {}
    for line in open(path):
        t = json.loads(line)
        key = rank(seed, t["sha256"])
        if key not in taken and int(key, 16) < p * 16**64:
            taken[key] = line
    for key in sorted(taken):
        print(taken[key], end="")


# Extracts a tar archive from stdin with untar from argv[1], into argv[2]
UNTAR = """
import errno, sys
sys.path.insert(0, sys.argv[1])
import untar
try:
    untar.extract(sys.stdin.buffer, sys.argv[2])
except untar.Error as e:
    print(e, file=sys.stderr)
    sys.exit(10)
except OSError as e:
    # Out of disk space says nothing about the archive. Other errors do: untar never replaces
    # an entry (O_EXCL), so an archive with names that collide here fails with EEXIST.
    print(f"{type(e).__name__}: {e}", file=sys.stderr)
    sys.exit(11 if e.errno in (errno.ENOSPC, errno.EDQUOT) else 10)
"""


class Untar:
    """untar in a child process, extracting the decompressed archive written to it."""

    def __init__(self, untar_path, dest):
        self.dest = dest
        self.process = subprocess.Popen(
            [sys.executable, "-I", "-c", UNTAR, untar_path, dest],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
        )
        self.stopped = False

    def write(self, chunk):
        if not self.stopped:
            try:
                self.process.stdin.write(chunk)
            except BrokenPipeError:
                # untar stopped reading: it rejected the archive
                self.stopped = True

    def result(self):
        """The outcome, as (error, skipped): error is None if untar extracted the archive."""
        try:
            self.process.stdin.close()
        except BrokenPipeError:
            pass
        stderr = self.process.stderr.read().decode(errors="replace").strip()
        code = self.process.wait()
        shutil.rmtree(self.dest, ignore_errors=True)
        if code == 0:
            return None, None
        if code == 10:
            return stderr, None
        if code == 11:
            return None, f"no disk space: {stderr}"
        return None, f"untar crashed: {stderr[-500:]}"


class Cache:
    """Tarballs named by their sha256 in a directory, up to a total size: the least recently used
    are removed first, and tarballs over a tenth of it are not kept. A file contains the URL the
    tarball was downloaded from on its first line, then the tarball. Its mtime is when it was
    last used: atime is unreliable.

    A run never removes the tarballs it used itself, and keeps no more once those fill the cache.
    Runs read tarballs in the same order, so with plain LRU, a run over more tarballs than fit
    would remove each one just before the next run needs it.

    Workers share the cache without locks. Files are written under a temporary name and renamed
    into place, and are read and touched through one file descriptor. A file is removed by
    renaming it to a temporary name first, so that the checks before removing it apply to the file
    that is removed: if they fail, it is linked back, unless a new copy took its name."""

    def __init__(self, path, size):
        self.path = path
        self.size = size
        self.since = time.time()
        os.makedirs(path, exist_ok=True)

    def dir(self):
        return os.open(self.path, os.O_RDONLY | os.O_DIRECTORY)

    def get(self, sha256):
        """The tarball, opened after its URL, and the URL; or None."""
        d = self.dir()
        try:
            fd = os.open(sha256, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=d)
        except FileNotFoundError:
            return None
        finally:
            os.close(d)
        os.utime(fd)
        f = os.fdopen(fd, "rb")
        return f, f.readline().decode(errors="replace").rstrip("\n")

    def remove(self, name, keep=lambda st: False):
        """Remove the file name, unless keep is true of it."""
        d = self.dir()
        try:
            claim = temporary_name()
            try:
                os.rename(name, claim, src_dir_fd=d, dst_dir_fd=d)
            except FileNotFoundError:
                return
            try:
                fd = os.open(claim, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=d)
            except OSError:
                # Not a file
                os.unlink(claim, dir_fd=d)
                return
            try:
                if keep(os.fstat(fd)):
                    try:
                        os.link(claim, name, src_dir_fd=d, dst_dir_fd=d, follow_symlinks=False)
                    except FileExistsError:
                        pass
            finally:
                os.close(fd)
            os.unlink(claim, dir_fd=d)
        finally:
            os.close(d)

    def evict(self, sha256, added):
        """Make room for the tarball just added, whose stat is added, or remove it if there is no
        room."""
        d = self.dir()
        try:
            entries = []
            for e in os.scandir(d):
                if len(e.name) == 64:
                    try:
                        st = e.stat(follow_symlinks=False)
                    except FileNotFoundError:
                        continue
                    entries.append((st.st_mtime, st.st_size, e.name))
        finally:
            os.close(d)
        total = sum(size for _, size, _ in entries)
        for mtime, size, name in sorted(entries):
            if total <= self.size or mtime >= self.since:
                break
            # Unless another worker used it since
            self.remove(name, keep=lambda st: st.st_mtime >= self.since)
            total -= size
        if total > self.size:
            # Unless another worker replaced it since
            self.remove(sha256, keep=lambda st: not same_file(st, added))

    def clean(self):
        """Remove partial downloads of runs that were killed: those not written to for a day."""
        d = self.dir()
        try:
            day_ago = time.time() - 86400
            for e in os.scandir(d):
                try:
                    old = e.name.startswith(".tmp-") and e.stat().st_mtime < day_ago
                except FileNotFoundError:
                    continue
                if old:
                    self.remove(e.name, keep=lambda st: st.st_mtime >= day_ago)
        finally:
            os.close(d)


def temporary_name():
    return f".tmp-{os.urandom(8).hex()}"


def same_file(a, b):
    return (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino)


class CacheWriter:
    """A copy of a download, kept in the cache if it is complete and its sha256 is right. Call
    keep or discard when the download is done."""

    def __init__(self, cache, url):
        self.cache = cache
        self.d = cache.dir()
        self.name = temporary_name()
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        self.f = os.fdopen(os.open(self.name, flags, 0o644, dir_fd=self.d), "wb")
        self.f.write(url.encode() + b"\n")
        self.size = 0

    def write(self, data):
        if self.f is None:
            return
        self.size += len(data)
        if self.size <= self.cache.size // 10:
            try:
                self.f.write(data)
                return
            except OSError:
                pass  # Out of disk space: scan without caching
        self._close()

    def _close(self):
        try:
            self.f.close()
        except OSError:
            pass
        self.f = None

    def keep(self, sha256):
        added = None
        try:
            if self.f is not None:
                self.f.flush()
                added = os.fstat(self.f.fileno())
                self._close()
                os.replace(self.name, sha256, src_dir_fd=self.d, dst_dir_fd=self.d)
                self.name = None
        except OSError:
            added = None
        finally:
            self.discard()
        if added is not None:
            self.cache.evict(sha256, added)

    def discard(self):
        """Remove the copy, unless it was kept, and close the directory."""
        if self.d is None:
            return
        if self.f is not None:
            self._close()
        if self.name is not None:
            try:
                os.unlink(self.name, dir_fd=self.d)
            except FileNotFoundError:
                pass
        os.close(self.d)
        self.d = None


class Hashing:
    """A binary file that hashes and counts what is read from it, and copies it to copy."""

    def __init__(self, f, copy=None):
        self.f = f
        self.copy = copy
        self.sha256 = hashlib.sha256()
        self.size = 0
        self.failed = None

    def read(self, n=-1):
        try:
            data = self.f.read(n)
        except Exception as e:
            self.failed = e
            raise
        self.sha256.update(data)
        self.size += len(data)
        if self.copy is not None:
            self.copy.write(data)
        return data


def member_of(f, t):
    """For a tarball listed with a `member`, as a gem is with `data.tar.gz`: the outer archive read
    from f whole, the member's data to scan, and what the scan finds of the outer archive."""
    outer = f.read()
    found = tarscan.scan(io.BytesIO(outer))
    with tarfile.open(fileobj=io.BytesIO(outer), mode="r:") as archive:
        data = archive.extractfile(t["member"]).read()
    return io.BytesIO(data), {"name": t["member"], "features": found["features"],
                              "error": found.get("error")}


def scan_tarball(raw, t, untar_path, workdir, copy=None):
    """Scan the tarball read from raw, and extract it with untar if a path is given. Return the
    result, or an error if it could not be read or its sha256 is wrong. For a tarball listed with a
    `member`, the sha256 is that of the outer archive, and the member is scanned and extracted."""
    untar = Untar(untar_path, os.path.join(workdir, "untar")) if untar_path else None
    result = {}
    downloaded = f = Hashing(raw, copy)
    try:
        start = time.time()
        try:
            if t.get("member"):
                inner, result["member_of"] = member_of(downloaded, t)
                f = Hashing(inner)
            result.update(tarscan.scan(f, untar.write if untar else None))
        except Exception as e:
            if downloaded.failed is not None:
                return None, f"{type(e).__name__}: {e}"
            if isinstance(e, (EOFError, zlib.error, lzma.LZMAError, OSError)):
                result["compression_error"] = f"{type(e).__name__}: {e}"
            elif isinstance(e, (tarfile.TarError, KeyError)) and "member_of" not in result:
                result["member_error"] = f"{type(e).__name__}: {e}"
            else:
                result["scan_crash"] = traceback.format_exc()
        while downloaded.read(1 << 20):
            pass
        result["scan_seconds"] = round(time.time() - start, 2)
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"
    finally:
        if untar:
            result["untar_error"], skipped = untar.result()
            if skipped:
                result["untar_skipped"] = skipped
    if downloaded.sha256.hexdigest() != t["sha256"]:
        return None, "sha256 mismatch"
    result["bytes"] = downloaded.size
    return result, None


def fetch_and_scan(url, t, untar_path, workdir, cache=None):
    """Scan the tarball at url while it downloads, and keep it in cache if one is given."""
    if not url.startswith(("https://", "http://", "ftp://")):
        return None, "not a URL to download from"
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    copy = CacheWriter(cache, url) if cache else None
    try:
        with urllib.request.urlopen(request, timeout=60) as r:
            result, error = scan_tarball(r, t, untar_path, workdir, copy)
    except Exception as e:
        result, error = None, f"{type(e).__name__}: {e}"
    if copy and error is None:
        copy.keep(t["sha256"])
    elif copy:
        copy.discard()
    return result, error


def scan_one(args):
    t, untar_path, cache = args
    result = dict(t, scanner=SCANNER)
    if untar_path:
        result["untar"] = version(os.path.join(untar_path, "untar.py"))
    workdir = tempfile.mkdtemp(prefix="scan-")
    try:
        cached = cache.get(t["sha256"]) if cache else None
        if cached:
            f, url = cached
            with f:
                scanned, error = scan_tarball(f, t, untar_path, workdir)
                if error is not None:
                    # Damaged: download it again, unless another worker replaced it since
                    st = os.fstat(f.fileno())
                    cache.remove(t["sha256"], keep=lambda other: not same_file(other, st))
            if error is None:
                result.update(scanned, source=url, cached=True)
                return result
        errors = []
        for url in t.get("urls") or [t["url"]]:
            scanned, error = fetch_and_scan(url, t, untar_path, workdir, cache)
            if error is None:
                result["source"] = url
                result.update(scanned)
                return result
            errors.append(f"{url}: {error}")
        result["download_error"] = errors
        return result
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def version(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()[:12]


def reusable(paths, untar_path):
    """Results in paths, by sha256, from this scanner and untar, where untar was not skipped."""
    untar = version(os.path.join(untar_path, "untar.py")) if untar_path else None
    found = {}
    for path in paths:
        for line in open(path):
            r = json.loads(line)
            if "features" in r and r.get("scanner") == SCANNER and r.get("untar") == untar \
                    and not r.get("untar_skipped"):
                found.setdefault(r["sha256"], r)
    return found


def scan(sample_path, out_path, untar_path=None, jobs=8, reuse=(), cache=None):
    done = set()
    if os.path.exists(out_path):
        done = {json.loads(line)["sha256"] for line in open(out_path)}
    todo = [json.loads(line) for line in open(sample_path)]
    todo = [t for t in todo if t["sha256"] not in done]
    known = reusable(reuse, untar_path)
    with open(out_path, "a") as out:
        for t in [t for t in todo if t["sha256"] in known]:
            r = known[t["sha256"]]
            copied = {k: r[k] for k in SCAN_FIELDS if k in r}
            out.write(json.dumps(dict(t, **copied, source=r.get("source"), reused=True)) + "\n")
    todo = [t for t in todo if t["sha256"] not in known]
    print(f"{len(done)} done, {len(todo)} to go", file=sys.stderr)
    if cache:
        cache.clean()
    with multiprocessing.Pool(jobs) as pool, open(out_path, "a") as out:
        for i, result in enumerate(
            pool.imap_unordered(scan_one, [(t, untar_path, cache) for t in todo]), 1
        ):
            out.write(json.dumps(result) + "\n")
            out.flush()
            if i % 50 == 0:
                print(f"{len(done) + i} done", file=sys.stderr)


def main():
    args = sys.argv[1:]
    if args[0] == "sample":
        sample(args[1], int(args[2]), int(args[3]))
    elif args[0] == "fraction":
        fraction(args[1], float(args[2]), int(args[3]))
    elif args[0] == "scan":
        untar_path = args[args.index("--untar") + 1] if "--untar" in args else None
        jobs = int(args[args.index("--jobs") + 1]) if "--jobs" in args else 8
        reuse = [args[i + 1] for i, a in enumerate(args) if a == "--reuse"]
        cache = None
        if "--cache" in args:
            gb = float(args[args.index("--cache-size") + 1]) if "--cache-size" in args else 50
            cache = Cache(args[args.index("--cache") + 1], int(gb * 1e9))
        scan(args[1], args[2], untar_path, jobs, reuse, cache)


if __name__ == "__main__":
    main()
