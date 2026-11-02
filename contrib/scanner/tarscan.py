"""Scan the headers of tar archives and report the features they use.

    python -I contrib/scanner/tarscan.py ARCHIVE...

prints one JSON object per archive. The scanner reads every header and skips all data. Unlike
an extractor, it does not stop at the first questionable feature: it counts every feature it
finds, with a few example names each, so that a strictness policy can be evaluated later as a
query over its output. Where implementations would frame the archive differently, it continues as
GNU tar would, and reports the disagreement.

Compressed archives (gzip, bzip2, xz) are decompressed on the fly. The compression layer is
described only briefly: the number of streams, and the bytes after the last one.
"""

import bz2
import collections
import json
import lzma
import re
import sys
import unicodedata
import zlib

BLOCK = 512
ZERO = bytes(BLOCK)
CHUNK = 1 << 16
MAX_OUTPUT = 1 << 22
MAX_EXTENDED = 1 << 24
HIGH_BYTES = bytes(range(128, 256))
EXAMPLES = 3


# Decompression


class Stream:
    """The decompressed bytes of a file, read in order."""

    MAGIC = {
        b"\x1f\x8b": "gzip",
        b"BZh": "bzip2",
        b"\xfd7zXZ\x00": "xz",
    }

    def __init__(self, raw, tee=None):
        self.raw = raw
        self.pending = raw.read(BLOCK + 1)
        self.format = next((f for m, f in self.MAGIC.items() if self.pending.startswith(m)), None)
        self.info = {"format": self.format or "none", "streams": 0, "trailing_bytes": 0}
        self.chunks = self._decompress() if self.format else self._plain()
        if tee is not None:
            self.chunks = self._tee(self.chunks, tee)
        self.buffer = b""
        self.pos = 0
        self.offset = 0

    def _raw(self):
        if self.pending:
            data, self.pending = self.pending, b""
            return data
        return self.raw.read(CHUNK)

    def _plain(self):
        while True:
            data = self._raw()
            if not data:
                return
            yield data

    def _decompressor(self):
        if self.format == "gzip":
            return zlib.decompressobj(31)
        if self.format == "bzip2":
            return bz2.BZ2Decompressor()
        return lzma.LZMADecompressor(lzma.FORMAT_XZ)

    def _decompress(self):
        while True:
            self.info["streams"] += 1
            d = self._decompressor()
            data = self._raw()
            while True:
                out = d.decompress(data, MAX_OUTPUT)
                if out:
                    yield out
                if d.eof:
                    break
                if self.format == "gzip":
                    data = d.unconsumed_tail or self._raw()
                    starved = not data
                else:
                    data = self._raw() if d.needs_input else b""
                    starved = d.needs_input and not data
                if starved:
                    self.info["truncated"] = True
                    return
            rest = d.unused_data
            while len(rest) < 8:
                more = self._raw()
                if not more:
                    break
                rest += more
            if self.format == "xz":
                padding = len(rest) - len(rest.lstrip(b"\0"))
                if rest[padding:].startswith(b"\xfd7zXZ\x00"):
                    self.info["xz_stream_padding"] = True
                    rest = rest[padding:]
            if rest[:6] and self.MAGIC.get(rest[: len(self._magic())]) == self.format:
                self.pending = rest
                continue
            # Whatever follows the last stream
            nonzero = False
            while rest:
                self.info["trailing_bytes"] += len(rest)
                nonzero = nonzero or rest.strip(b"\0") != b""
                rest = self._raw()
            if self.info["trailing_bytes"]:
                self.info["trailing_nonzero"] = nonzero
            return

    @staticmethod
    def _tee(chunks, tee):
        for chunk in chunks:
            tee(chunk)
            yield chunk

    def drain(self):
        """Read the rest of the stream, for its tee and the description of its compression."""
        for _ in self.chunks:
            pass

    def _magic(self):
        return next(m for m, f in self.MAGIC.items() if f == self.format)

    def read(self, n):
        while len(self.buffer) - self.pos < n:
            chunk = next(self.chunks, None)
            if chunk is None:
                break
            self.buffer = self.buffer[self.pos :] + chunk
            self.pos = 0
        data = self.buffer[self.pos : self.pos + n]
        self.pos += len(data)
        self.offset += len(data)
        return data

    def skip(self, n):
        """Skip n bytes, and return how many were skipped."""
        skipped = min(n, len(self.buffer) - self.pos)
        self.pos += skipped
        while skipped < n:
            chunk = next(self.chunks, None)
            if chunk is None:
                break
            take = min(n - skipped, len(chunk))
            skipped += take
            self.buffer, self.pos = chunk, take
        self.offset += skipped
        return skipped


# Fields


def pattern(field):
    """The shape of a number field: runs of octal digits (d), other digits (9), spaces (s),
    NULs (n) and other bytes (x)."""
    shape = []
    for b in field:
        c = (
            "d"
            if 48 <= b <= 55
            else "9"
            if 56 <= b <= 57
            else "s"
            if b == 32
            else "n"
            if b == 0
            else "x"
        )
        if not shape or shape[-1] != c:
            shape.append(c)
    return "".join(shape)


def octal_cut(field):
    """The value as an implementation that cuts the field at its first NUL reads it (Python's
    tarfile)."""
    s = field.split(b"\0", 1)[0].strip(b" ")
    if not s:
        return 0
    return int(s, 8) if all(48 <= b <= 55 for b in s) else None


def octal_skip(field):
    """The value as an implementation that skips leading spaces and NULs reads it (GNU tar's
    leniency)."""
    s = field.lstrip(b" \0")
    m = re.match(rb"[0-7]*", s)
    return int(m.group(), 8) if m.group() else None


def number(field, name, features):
    """Parse a number field, report how it is written, and return its value."""
    if field[0] in (0x80, 0xFF):
        n = int.from_bytes(field[1:], "big")
        if field[0] == 0xFF:
            n -= 256 ** (len(field) - 1)
        features.add(f"number.{name}.base256" + ("-negative" if n < 0 else ""))
        if abs(n) >= 1 << 63:
            features.add(f"number.{name}.base256-too-large")
        return n, "b256"
    shape = pattern(field)
    if shape.startswith("n") and "d" in shape:
        features.add(f"number.{name}.leading-nul")
    if shape.startswith("s") and "d" in shape:
        features.add(f"number.{name}.leading-space")
    if "d" not in shape:
        features.add(f"number.{name}.no-digits")
    elif re.search(r"d[sn]+d", shape):
        features.add(f"number.{name}.gap-in-digits")
    if shape == "d":
        features.add(f"number.{name}.no-terminator")
    if "9" in shape or "x" in shape:
        features.add(f"number.{name}.invalid-character")
    cut, skip = octal_cut(field), octal_skip(field)
    if cut is not None and skip is not None and cut != skip:
        features.add(f"number.{name}.readers-differ")
    return (skip if skip is not None else 0), shape


def cstring(field, name, features):
    """A NUL-terminated string field."""
    s, nul, rest = field.partition(b"\0")
    if not nul:
        features.add(f"{name}.no-nul")
    elif rest.strip(b"\0"):
        features.add(f"{name}.bytes-after-nul")
    return s


# Pax records


def pax_records(data, features, kind):
    """The records of a pax header, in order, as (key, value) pairs."""
    records = []
    keys = set()
    pos = 0
    while pos < len(data):
        if not data[pos:].strip(b"\0"):
            features.add(f"{kind}.trailing-nuls")
            break
        space = data.find(b" ", pos)
        length = data[pos:space] if space >= 0 else b""
        if not length.isdigit() or len(length.lstrip(b"0")) > 9:
            features.add(f"{kind}.invalid-length")
            break
        if length.startswith(b"0"):
            features.add(f"{kind}.length-leading-zero")
        end = pos + int(length)
        if end > len(data) or end <= space + 1:
            features.add(f"{kind}.invalid-length")
            break
        record = data[space + 1 : end]
        if record.endswith(b"\n"):
            record = record[:-1]
        else:
            features.add(f"{kind}.no-newline")
        key, eq, value = record.partition(b"=")
        if not eq:
            features.add(f"{kind}.no-equals")
        if key != key.strip():
            features.add(f"{kind}.key-whitespace")
        if not key.strip():
            features.add(f"{kind}.empty-key")
        if b"\n" in value:
            features.add(f"{kind}.newline-in-value.{key_family(key)}")
        if b"\0" in value:
            features.add(f"{kind}.nul-in-value.{key_family(key)}")
        if not value:
            features.add(f"{kind}.empty-value.{key_family(key)}")
        if key != b"path":
            try:
                value.decode("utf-8")
            except UnicodeDecodeError:
                features.add(f"{kind}.value-not-utf8.{key_family(key)}")
        if key in keys:
            features.add(f"{kind}.repeated-key")
        keys.add(key)
        records.append((key, value))
        pos = end
    return records


def key_family(key):
    key = key.decode("utf-8", "backslashreplace")
    for prefix in ("LIBARCHIVE.xattr.", "SCHILY.xattr.", "SCHILY.acl.", "GNU.sparse."):
        if key.startswith(prefix):
            return prefix + "*"
    return key


def decode(name):
    return name.decode("utf-8", "backslashreplace")[:200]


# Names


def normalize(name):
    """The path a name refers to: without ./, empty components and trailing slashes."""
    parts = [p for p in name.split(b"/") if p not in (b"", b".")]
    return b"/".join(parts)


def name_features(name, kind, features):
    if not name:
        features.add("name.empty")
        return
    if name.startswith(b"/"):
        features.add("name.absolute")
    parts = name.split(b"/")
    if b".." in parts:
        features.add("name.dotdot")
    if name.startswith(b"./"):
        features.add("name.leading-dot-slash")
    if name in (b".", b"./"):
        features.add("name.dot")
    if b"//" in name.strip(b"/"):
        features.add("name.double-slash")
    if b"." in parts[1:]:
        features.add("name.dot-component")
    if b"\\" in name:
        features.add("name.backslash")
    if re.match(rb"[A-Za-z]:", name):
        features.add("name.drive-letter")
    if name.endswith(b"/") and kind != "dir":
        features.add(f"name.trailing-slash-on-{kind}")
    if kind == "dir" and not name.endswith(b"/"):
        features.add("name.dir-without-trailing-slash")
    if any(b < 32 or b == 127 for b in name):
        features.add("name.control-character")
    windows_features(parts, features)
    try:
        text = name.decode("utf-8")
    except UnicodeDecodeError:
        features.add("name.not-utf8")
        return
    if not text.isascii():
        features.add("name.non-ascii")
        if unicodedata.normalize("NFC", text) != text:
            features.add("name.not-nfc")


WINDOWS_RESERVED = re.compile(rb"(con|prn|aux|nul|com[0-9]|lpt[0-9])(\.[^.]*)?", re.IGNORECASE)
WINDOWS_INVALID = re.compile(rb'[<>:"|?*\x00-\x1f]')


def windows_features(parts, features):
    """Names that Windows cannot create: they fail there, and nowhere else."""
    for part in parts:
        if part in (b"", b".", b".."):
            continue
        if WINDOWS_RESERVED.fullmatch(part):
            features.add("platform.windows-reserved-name")
        if WINDOWS_INVALID.search(part):
            features.add("platform.windows-invalid-character")
        if part.endswith((b".", b" ")):
            features.add("platform.windows-trailing-dot-or-space")


# The archive


KINDS = {
    b"0": "file",
    b"\0": "file",
    b"7": "file",
    b"1": "hardlink",
    b"2": "symlink",
    b"3": "chardev",
    b"4": "blockdev",
    b"5": "dir",
    b"6": "fifo",
}
EXTENDED = (b"x", b"X", b"g", b"L", b"K")


class Features:
    """Counts of features in one archive, with example member names."""

    def __init__(self):
        self.counts = collections.Counter()
        self.examples = collections.defaultdict(list)
        self.name = None

    def add(self, feature, name=None):
        self.counts[feature] += 1
        example = name if name is not None else self.name
        if example is not None and len(self.examples[feature]) < EXAMPLES:
            self.examples[feature].append(decode(example))


class Scanner:
    def __init__(self, stream):
        self.stream = stream
        self.features = Features()
        self.fingerprint = collections.defaultdict(collections.Counter)
        self.members = 0
        self.kinds = collections.Counter()
        self.mtimes = []
        self.pending = []  # extended headers for the next member, as (type, data, name)
        self.paths = {}  # normalized path -> kind
        self.raw_names = set()
        self.implied = set()
        self.nfc = {}
        self.folded = {}
        self.unresolved = []  # hardlinks whose target is not an earlier member
        self.first_format = None  # of the first header, by which some readers decide the format
        self.error = None

    def run(self):
        try:
            self._run()
        except Error as e:
            self.error = str(e)
        self._finish()
        return self.result()

    def _run(self):
        block = self.stream.read(BLOCK)
        while True:
            if not block:
                self.features.add("end.missing" if self.members else "archive.empty")
                return
            if len(block) < BLOCK:
                raise Error("truncated in a header")
            if block == ZERO:
                block = self.stream.read(BLOCK)
                if block == ZERO:
                    self._after_end()
                    return
                if not block:
                    self.features.add("end.lone-zero-block")
                    return
                self.features.add("end.zero-block-before-member")
                continue
            self._header(block)
            block = self.stream.read(BLOCK)

    def _after_end(self):
        """What follows the end-of-archive marker: zeros, another archive, or other data."""
        offset = self.stream.offset
        zeros = 0
        while True:
            block = self.stream.read(BLOCK)
            if not block:
                break
            if len(block) < BLOCK:
                self.features.add("end.partial-block")
                if block.strip(b"\0"):
                    self.features.add("end.data-after")
                break
            if block == ZERO:
                zeros += 1
                continue
            if valid_checksum(block):
                self.features.add("end.archive-after", block[:100].split(b"\0", 1)[0])
            else:
                self.features.add("end.data-after")
            break
        padded = (offset + zeros * BLOCK) % 10240 == 0
        self.fingerprint["end"]["padded-to-10240" if padded else "unpadded"] += 1
        self.fingerprint["zero_blocks_after_end"][str(min(zeros, 20))] += 1

    def _header(self, block):
        features = self.features
        features.name = block[:100].split(b"\0", 1)[0]
        checksum_field = block[148:156]
        self.fingerprint["checksum"][pattern(checksum_field)] += 1
        if pattern(checksum_field).startswith("s") and "d" in pattern(checksum_field):
            features.add("number.chksum.leading-space")
        stored = octal_skip(checksum_field)
        unsigned = sum(block) - sum(checksum_field) + 8 * 32
        signed = unsigned - 256 * (BLOCK - len(block.translate(None, HIGH_BYTES)))
        if stored != unsigned:
            if stored == signed:
                features.add("checksum.signed")
            else:
                raise Error(f"invalid checksum at offset {self.stream.offset - BLOCK}")

        magic = block[257:265]
        if magic[:6] == b"ustar\0":
            fmt = "posix" if magic[6:] == b"00" else "posix-version-" + magic[6:].hex()
        elif magic == b"ustar  \0":
            fmt = "gnu"
        elif not magic.strip(b"\0"):
            fmt = "v7"
        else:
            fmt = "other"
            features.add("magic.other")
        if fmt == "posix-version-0000":
            features.add("magic.posix-version-nuls")
        elif fmt.startswith("posix-version"):
            features.add("magic.posix-with-odd-version")
        if fmt == "posix" and block[508:512] == b"tar\0":
            fmt = "star"
        self.fingerprint["magic"][fmt] += 1
        if self.first_format is None:
            self.first_format = fmt

        type = block[156:157]
        if type in (b"x", b"g", b"X") and self.first_format == "v7":
            features.add("format.pax-after-v7")
        size, size_shape = number(block[124:136], "size", features)
        self.fingerprint["size"][size_shape] += 1
        for field, start, end in (
            ("mode", 100, 108),
            ("uid", 108, 116),
            ("gid", 116, 124),
            ("mtime", 136, 148),
        ):
            value, shape = number(block[start:end], field, features)
            self.fingerprint[field][shape] += 1
            if field == "mtime" and type not in EXTENDED:
                self.mtimes.append(value)
        if fmt != "v7" and type not in EXTENDED:
            for field, start in (("devmajor", 329), ("devminor", 337)):
                self.fingerprint[field][pattern(block[start : start + 8])] += 1
            self.fingerprint["uname"][decode(block[265:297].split(b"\0", 1)[0])] += 1

        if size < 0:
            raise Error("negative size")

        if type in EXTENDED:
            self._extended(type, block, size)
            return

        if type == b"S" and fmt == "gnu":
            features.add("type.gnu-sparse")
            extension = block[482]
            while extension:
                ext = self.stream.read(BLOCK)
                if len(ext) < BLOCK:
                    raise Error("truncated in a sparse header")
                extension = ext[504]
        self._member(type, block, fmt, size)

    def _extended(self, type, block, size):
        features = self.features
        name = block[:100].split(b"\0", 1)[0]
        if size > MAX_EXTENDED:
            raise Error(f"extended header of {size} bytes")
        data = self.stream.read(size)
        if len(data) < size:
            raise Error("truncated in an extended header")
        self.stream.skip(-size % BLOCK)
        if type == b"X":
            features.add("type.solaris-extended")
        if type in b"xX":
            self.fingerprint["pax_header_name"][header_name_pattern(name)] += 1
        elif type in b"LK":
            self.fingerprint["gnu_long_name"][decode(name)] += 1
        if type == b"g":
            records = pax_records(data, features, "pax-global")
            if self.members:
                features.add("pax-global.after-members")
            if self.pending:
                features.add("pax-global.between-extended-and-member")
            for key, value in records:
                self.fingerprint["pax_global_keys"][key_family(key)] += 1
                if key in (b"path", b"linkpath", b"size"):
                    features.add(f"pax-global.{decode(key)}")
                if key == b"comment" and re.fullmatch(rb"[0-9a-f]{40}([0-9a-f]{24})?", value):
                    self.fingerprint["producer_hint"]["git-archive"] += 1
            self.fingerprint["pax_global_header_name"][decode(name)] += 1
            return
        if type in b"xX":
            self.pending.append(("x", pax_records(data, features, "pax"), name))
        else:
            self.pending.append((type.decode(), data, name))

    def _member(self, type, block, fmt, size):
        features = self.features
        pending, self.pending = self.pending, []
        kind = KINDS.get(type)
        if kind is None:
            features.add(f"type.unknown-{decode(type)}")
            kind = "file"
        elif type == b"7":
            features.add("type.contiguous")
        elif type == b"\0":
            features.add("type.nul")

        # The name, from every source
        name, nul, _ = block[:100].partition(b"\0")
        linkname = cstring(block[157:257], "linkname", features)
        prefix = b""
        if fmt == "posix":
            prefix = block[345:500].split(b"\0", 1)[0]
        elif fmt == "star":
            prefix = block[345:476].split(b"\0", 1)[0]
            features.add("format.star")
        elif fmt == "gnu":
            if block[345:369].strip(b"\0"):
                features.add("gnu.atime-ctime")
            if block[369:500].strip(b"\0") and type != b"S":
                features.add("gnu.offset-or-sparse-fields")
        elif fmt == "v7" and block[257:512].strip(b"\0"):
            features.add("v7.bytes-after-linkname")
        if prefix:
            features.add("ustar.prefix")
        header_name = prefix + b"/" + name if prefix else name

        seq = "".join(t for t, _, _ in pending)
        self.fingerprint["extended_sequence"][seq or "-"] += 1
        pax = {}
        pax_names, long_names, long_links = [], [], []
        for t, data, _ in pending:
            if t == "x":
                for key, value in data:
                    self.fingerprint["pax_keys"][key_family(key)] += 1
                    if key in pax:
                        features.add(f"pax.key-in-two-headers.{key_family(key)}", header_name)
                    pax[key] = value
                    if key == b"path":
                        pax_names.append(value)
            else:
                text, nul, rest = data.partition(b"\0")
                if not text:
                    features.add("gnu-long.empty", header_name)
                if not nul:
                    features.add("gnu-long.no-nul", header_name)
                elif rest.strip(b"\0"):
                    features.add("gnu-long.nul-inside", header_name)
                (long_names if t == "L" else long_links).append(text)
        if seq.count("x") > 1:
            features.add("extended.two-pax-headers", header_name)
        if len(long_names) > 1:
            features.add("extended.two-gnu-long-names", header_name)
        if len(long_links) > 1:
            features.add("extended.two-gnu-long-links", header_name)
        if "x" in seq and ("L" in seq or "K" in seq):
            features.add("extended.gnu-long-and-pax", header_name)
        if pax_names and long_names:
            features.add("extended.pax-path-and-gnu-long-name", header_name)
        if b"linkpath" in pax and long_links:
            features.add("extended.pax-linkpath-and-gnu-long-link", header_name)
        if re.search("x.*[LK]", seq) and any(
            t == "x" and any(k == b"size" for k, _ in d) for t, d, _ in pending[:-1]
        ):
            features.add("extended.pax-size-before-gnu-long", header_name)
        candidates = set(pax_names + long_names) or {header_name}
        if len(candidates) > 1:
            features.add("extended.names-disagree", header_name)
        if b"path" in pax:
            name = pax[b"path"]
        elif long_names:
            name = long_names[-1]
        else:
            name = header_name
            if not nul:
                features.add("name.fills-field")
            if block[:100].partition(b"\0")[2].strip(b"\0"):
                features.add("name.bytes-after-nul")
        if b"linkpath" in pax:
            linkname = pax[b"linkpath"]
        elif long_links:
            linkname = long_links[-1]
        features.name = name

        if b"size" in pax:
            value = pax[b"size"]
            if not value.isdigit():
                features.add("pax.invalid-size")
            else:
                if value.startswith(b"0") and value != b"0":
                    features.add("pax.size-leading-zero")
                if len(value.lstrip(b"0")) > 19 or int(value) >= 1 << 63:
                    features.add("pax.size-too-large")
                    raise Error("a pax size of 2^63 or more")
                if int(value) != size and size != 0 and size_shape_is_octal(block[124:136]):
                    features.add("pax.size-disagrees")
                size = int(value)
                if kind not in ("file",):
                    features.add(f"pax.size-on-{kind}")
        if b"hdrcharset" in pax:
            features.add("pax.hdrcharset")
        for key in pax:
            if key.startswith(b"GNU.sparse."):
                features.add("pax.gnu-sparse")
            if key in (b"SCHILY.filetype", b"SCHILY.realsize", b"SUN.holesdata"):
                features.add(f"pax.{decode(key)}")
            if key.startswith(b"LIBARCHIVE.") and not key.startswith(b"LIBARCHIVE.xattr."):
                features.add(f"pax.{decode(key)}")
        if b"path" in pax:
            try:
                pax[b"path"].decode("utf-8")
            except UnicodeDecodeError:
                features.add("pax.path-not-utf8")
        if b"linkpath" not in pax and linkname and kind in ("hardlink", "symlink"):
            try:
                linkname.decode("utf-8")
            except UnicodeDecodeError:
                features.add("linkname.not-utf8")
        if (b"linkpath" in pax or long_links) and kind not in ("hardlink", "symlink"):
            features.add(f"extended.linkpath-on-{kind}")
        if linkname and kind not in ("hardlink", "symlink"):
            features.add(f"linkname.on-{kind}")
        if b"mtime" in pax:
            m = re.match(rb"-?\d+", pax[b"mtime"])
            if m:
                self.mtimes.append(int(m.group()))

        # The member
        self.members += 1
        self.kinds[kind] += 1
        name_features(name, kind, features)
        if size and kind not in ("file",):
            features.add(f"size.on-{kind}")
        if kind == "symlink":
            self._symlink(name, linkname)
        self._tree(name, kind, linkname)
        if kind == "file" or size:
            if self.stream.skip(size + (-size % BLOCK)) < size:
                raise Error("truncated in member data")

    def _symlink(self, name, target):
        features = self.features
        if not target:
            features.add("symlink.empty-target")
        elif target.startswith(b"/"):
            features.add("symlink.absolute")
        else:
            depth = len(normalize(name).split(b"/")) - 1
            for part in target.split(b"/"):
                if part == b"..":
                    depth -= 1
                    if depth < 0:
                        features.add("symlink.escapes")
                        break
                elif part not in (b"", b"."):
                    depth += 1

    def _tree(self, name, kind, linkname):
        features = self.features
        key = normalize(name)
        self.raw_names.add(name)
        parts = key.split(b"/")
        for i in range(1, len(parts)):
            parent = b"/".join(parts[:i])
            parent_kind = self.paths.get(parent)
            if parent_kind is None:
                self.implied.add(parent)
            elif parent_kind == "symlink":
                features.add("tree.through-symlink")
                break
            elif parent_kind != "dir":
                features.add(f"tree.under-{parent_kind}")
                break
        if key in self.paths:
            features.add(f"tree.duplicate.{self.paths[key]}-{kind}")
        elif kind == "dir" and key in self.implied:
            features.add("tree.dir-after-contents")
        if kind == "hardlink":
            target = normalize(linkname)
            if target == key:
                features.add("hardlink.to-itself")
            elif target in self.paths:
                target_kind = self.paths[target]
                if target_kind != "file":
                    features.add(f"hardlink.to-{target_kind}")
                if linkname not in self.raw_names:
                    features.add("hardlink.target-spelled-differently")
            else:
                self.unresolved.append((name, target))
        try:
            text = key.decode("utf-8")
        except UnicodeDecodeError:
            text = None
        if text is not None and key and key not in self.paths:
            nfc = unicodedata.normalize("NFC", text)
            folded = nfc.casefold()
            other = self.nfc.get(nfc)
            if other is not None and other != key:
                features.add("platform.normalization-collision")
            other = self.folded.get(folded)
            if other is not None and other != key and self.nfc.get(nfc) is None:
                features.add("platform.case-collision")
            self.nfc.setdefault(nfc, key)
            self.folded.setdefault(folded, key)
        self.paths[key] = kind

    def _finish(self):
        if self.pending:
            self.features.add("extended.without-member")

    def result(self):
        for name, target in self.unresolved:
            self.features.add(
                "hardlink.to-later-member" if target in self.paths else "hardlink.missing-target",
                name,
            )
        mtimes = sorted(self.mtimes)
        return {
            "members": self.members,
            "kinds": dict(self.kinds),
            "features": dict(self.features.counts),
            "examples": dict(self.features.examples),
            "fingerprint": {k: dict(v.most_common(8)) for k, v in self.fingerprint.items()},
            "mtime": [mtimes[0], mtimes[len(mtimes) // 2], mtimes[-1]] if mtimes else None,
            "error": self.error,
        }


def header_name_pattern(name):
    """The name of an extended header, with the member's own path components replaced by *."""
    parts = []
    for part in decode(name).split("/"):
        if part not in ("", ".") and "pax" not in part.lower() and "@" not in part:
            part = "*"
        part = re.sub(r"\d+", "N", re.sub(r"[0-9a-f]{16,}", "H", part))
        if not (part == "*" and parts and parts[-1] == "*"):
            parts.append(part)
    return "/".join(parts)


def size_shape_is_octal(field):
    return field[0] not in (0x80, 0xFF)


def valid_checksum(block):
    stored = octal_skip(block[148:156])
    return stored == sum(block) - sum(block[148:156]) + 8 * 32


class Error(Exception):
    pass


def scan(raw, tee=None):
    """Scan the archive in the binary file raw. If given, tee is called with every chunk of the
    decompressed archive, all of which is read, also where the scan stops early."""
    stream = Stream(raw, tee)
    scanner = Scanner(stream)
    result = scanner.run()
    if tee is not None:
        stream.drain()
    result["compression"] = stream.info
    return result


def main():
    for path in sys.argv[1:]:
        with open(path, "rb") as f:
            result = scan(f)
        print(json.dumps({"path": path, **result}))


if __name__ == "__main__":
    main()
