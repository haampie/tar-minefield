"""Build tar archives from raw 512-byte blocks, and describe every block as it is written.

The cases of the test suite use this instead of tarfile or any other implementation under test: it
writes exactly the bytes it is given, and normalizes nothing. Every field of a header is either
a value, which it encodes the usual way, or raw bytes, which it writes as they are. The dump of an
archive comes from what was written, so it does not parse the archive.
"""

BLOCK = 512

# (field, offset, width) of a ustar header
FIELDS = [
    ("name", 0, 100),
    ("mode", 100, 8),
    ("uid", 108, 8),
    ("gid", 116, 8),
    ("size", 124, 12),
    ("mtime", 136, 12),
    ("chksum", 148, 8),
    ("typeflag", 156, 1),
    ("linkname", 157, 100),
    ("magic", 257, 6),
    ("version", 263, 2),
    ("uname", 265, 32),
    ("gname", 297, 32),
    ("devmajor", 329, 8),
    ("devminor", 337, 8),
    ("prefix", 345, 155),
    ("pad", 500, 12),
]
NUMBERS = ("mode", "uid", "gid", "size", "mtime", "devmajor", "devminor")
TYPES = {
    b"0": "regular file",
    b"\0": "regular file (pre-POSIX)",
    b"1": "hardlink",
    b"2": "symlink",
    b"5": "directory",
    b"x": "pax extended header, for the next member",
    b"g": "pax global header",
    b"L": "GNU long name, for the next member",
    b"K": "GNU long link name, for the next member",
}


def octal(value, width):
    """value in octal, padded with zeros, and ended by a NUL: the usual encoding."""
    return b"%0*o\0" % (width - 1, value)


def pax_record(key, value):
    """A pax record, `<length> <key>=<value>\\n`, whose length counts itself."""
    body = b" " + key + b"=" + value + b"\n"
    length = len(body) + 1
    while len(b"%d" % length) + len(body) != length:
        length += 1
    return b"%d" % length + body


def show(raw):
    """Bytes as a string literal, with a run of NULs at the end counted rather than written."""
    stripped = raw.rstrip(b"\0")
    nuls = len(raw) - len(stripped)
    text = ""
    for b in stripped:
        c = chr(b)
        if c == "\\":
            text += "\\\\"
        elif c == '"':
            text += '\\"'
        elif c == "\0":
            text += "\\0"
        elif c == "\n":
            text += "\\n"
        elif 32 <= b < 127:
            text += c
        else:
            text += f"\\x{b:02x}"
    parts = [f'"{text}"'] if stripped else []
    if nuls:
        parts.append(f"{nuls} NUL" if nuls > 1 or not stripped else "NUL")
    return " + ".join(parts) if parts else '""'



def clip(line, n):
    """A line of at most n characters and an ellipsis, cut where show() has not written an escape:
    a cut inside one would show a different byte."""
    out, i = "", 0
    while i < len(line):
        width = (4 if line[i + 1:i + 2] == "x" else 2) if line[i] == "\\" else 1
        if len(out) + width > n:
            break
        out += line[i:i + width]
        i += width
    return out + "…"

class Archive:
    def __init__(self):
        self.blocks = []  # (bytes, title, [(field, offset, width, raw, meaning)] or text lines)
        self.size = 0

    def _add(self, data, title, details):
        assert len(data) % BLOCK == 0
        self.blocks.append((self.size, data, title, details))
        self.size += len(data)

    def header(self, name, typeflag=b"0", size=0, note="", **raw):
        """A ustar header. Fields not given are the usual ones: mode 644 for files and 755 for
        directories, uid and gid 0, mtime 0, empty names, and the POSIX magic `ustar\\0` with
        version `00`. A keyword with bytes for a field writes those bytes as they are, padded
        with NULs; the checksum is computed, unless it is given too."""
        values = {
            "name": name,
            "mode": 0o755 if typeflag == b"5" else 0o644,
            "uid": 0,
            "gid": 0,
            "size": size,
            "mtime": 0,
            "typeflag": typeflag,
            "linkname": b"",
            "magic": b"ustar\0",
            "version": b"00",
            "uname": b"",
            "gname": b"",
            "devmajor": 0,
            "devminor": 0,
            "prefix": b"",
            "pad": b"",
        }
        for key, value in raw.items():
            if key != "chksum":
                assert key in values, key
                values[key] = value
        block = bytearray(BLOCK)
        fields = []
        for field, offset, width in FIELDS:
            if field == "chksum":
                continue
            value = values[field]
            if isinstance(value, int):
                encoded = octal(value, width)
                meaning = f"{value:o} (octal)" if field == "mode" else str(value)
            else:
                encoded, meaning = value, ""
            assert len(encoded) <= width, (field, encoded)
            block[offset : offset + len(encoded)] = encoded
            if field == "typeflag":
                meaning = TYPES.get(value, "unknown typeflag")
            fields.append((field, offset, width, meaning))
        if raw.get("chksum") == "signed":
            block[148:156] = b" " * 8
            total = sum(b - 256 if b > 127 else b for b in block)
            chksum = b"%06o\0 " % total
            meaning = f"{total}: the signed sum of the header, as some old tars computed it"
        elif raw.get("chksum") == "leading-space":
            block[148:156] = b" " * 8
            total = sum(block)
            chksum = b"%6o\0 " % total
            meaning = f"{total}: the unsigned sum, padded with spaces, as Perl's Archive::Tar writes it"
        elif "chksum" in raw:
            chksum, meaning = raw["chksum"], "given"
        else:
            block[148:156] = b" " * 8
            total = sum(block)
            chksum = b"%06o\0 " % total
            meaning = f"{total}: the unsigned sum of the header, this field as spaces"
        block[148 : 148 + len(chksum)] = chksum
        fields.append(("chksum", 148, 8, meaning))
        fields.sort(key=lambda f: f[1])
        # fields that the case writes itself: as raw bytes, or by a keyword
        explicit = set(raw) | {k for k in NUMBERS if isinstance(values[k], bytes)}
        details = [(f, o, w, bytes(block[o : o + w]), m, f in explicit) for f, o, w, m in fields]
        title = f"header: {TYPES.get(typeflag, 'unknown type')}" + (f", {note}" if note else "")
        self._add(bytes(block), title, details)
        return self

    def data(self, content, note=""):
        """The data of a member, padded with NULs to a whole block."""
        if not content:
            return self
        padded = content + bytes(-len(content) % BLOCK)
        lines = [f"{len(content)} bytes, then {len(padded) - len(content)} NUL to the end of the block"]
        if content:
            lines.append(show(content) if len(content) <= 400 else show(content[:400]) + " ...")
        self._add(padded, "data" + (f": {note}" if note else ""), lines)
        return self

    def file(self, name, content, note="", **raw):
        size = raw.pop("size", len(content))
        return self.header(name, b"0", size, note, **raw).data(content)

    def directory(self, name, note="", **raw):
        return self.header(name, b"5", 0, note, **raw)

    def symlink(self, name, target, note="", **raw):
        return self.header(name, b"2", 0, note, linkname=target, **raw)

    def hardlink(self, name, target, note="", **raw):
        return self.header(name, b"1", 0, note, linkname=target, **raw)

    def pax(self, records, typeflag=b"x", name=b"PaxHeader", note=""):
        """A pax extended (x) or global (g) header with the records given as (key, value)."""
        data = b"".join(pax_record(k, v) for k, v in records)
        self.header(name, typeflag, len(data), note)
        lines = [f"{len(data)} bytes of pax records, then {-len(data) % BLOCK} NUL"]
        lines += [show(pax_record(k, v)) for k, v in records]
        self._add(data + bytes(-len(data) % BLOCK), "data: pax records", lines)
        return self

    def gnu_long(self, name, typeflag=b"L", note=""):
        """A GNU long name (L) or long link name (K) for the next member, ended by a NUL."""
        data = name + b"\0"
        self.header(b"././@LongLink", typeflag, len(data), note, magic=b"ustar ", version=b" \0")
        lines = [f"{len(data)} bytes: the name and a NUL, then {-len(data) % BLOCK} NUL", show(data)]
        self._add(data + bytes(-len(data) % BLOCK), "data: GNU long name", lines)
        return self

    def raw(self, data, title):
        """Bytes as they are, padded with NULs to a whole block."""
        padded = data + bytes(-len(data) % BLOCK)
        self._add(padded, title, [f"{len(data)} bytes, then {len(padded) - len(data)} NUL", show(data)])
        return self

    def zeros(self, count=1, note=""):
        title = f"{count} zero block{'s' if count > 1 else ''}" + (f": {note}" if note else "")
        self._add(bytes(BLOCK * count), title, [])
        return self

    def end(self):
        return self.zeros(2, "the end-of-archive marker")

    def bytes(self):
        return b"".join(data for _, data, _, _ in self.blocks)

    def dump(self):
        """Every block: its offset, what it is, and for a header every field, as written."""
        out = []
        for offset, data, title, details in self.blocks:
            out.append(f"{offset:#08x}  {title}")
            for d in details:
                if isinstance(d, str):
                    out.append(f"          {d}")
                else:
                    field, start, width, raw, meaning, _ = d
                    line = f"          {field:<9}[{start:3},{start + width:3})  {show(raw)}"
                    out.append(line + (f"  {meaning}" if meaning else ""))
        out.append(f"{self.size:#08x}  end of file")
        return "\n".join(out) + "\n"


# The block map: every block a row of its 512 bytes, at a fixed width per byte, so that fields
# are where they are in the archive. Bytes are coloured by their class, in runs of one class:
# (class, colour, what it is).
BYTE_CLASSES = [
    ("nul", "#ffffff", "NUL"),
    ("text", "#54aeff", "printable ASCII"),
    ("space", "#b6e3ff", "space"),
    ("control", "#fb8f44", "control character, such as a newline"),
    ("high", "#c297ff", "byte over 0x7f"),
]
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"


def byte_class(b):
    if b == 0:
        return "nul"
    if b == 32:
        return "space"
    if b < 32 or b == 127:
        return "control"
    return "high" if b > 127 else "text"


def esc(text):
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def runs(data, x, y, scale, h):
    """The bytes of data as rectangles, one per run of bytes of one class."""
    out, start = [], 0
    for i in range(1, len(data) + 1):
        if i == len(data) or byte_class(data[i]) != byte_class(data[start]):
            cls = byte_class(data[start])
            if cls != "nul":
                out.append(f'<rect class="{cls}" x="{x + start * scale:g}" y="{y}" '
                           f'width="{(i - start) * scale:g}" height="{h}"/>')
            start = i
    return "".join(out)


def callouts(items, left, right, y):
    """Texts in monospace at the x of what they are about, packed into as few lines as fit
    without overlapping, from y down: (svg, the y below them)."""
    lines, out = [], []
    for x, text, cls in items:
        w = 6.6 * len(text)
        x = min(x, right - w)
        for i, end in enumerate(lines):
            if x >= end + 12:
                lines[i] = x + w
                break
        else:
            i = len(lines)
            lines.append(x + w)
        out.append(f'<text class="{cls}" x="{x:g}" y="{y + 12 + 14 * i}">{esc(text)}</text>')
    return "".join(out), y + 14 * len(lines) + (4 if lines else 0)


def block_map(archive, title):
    """The archive as an SVG: a row per block, with its offset and what it is, and its bytes to
    scale. In headers, every field is at its offset and named where the name fits, and has its
    bytes and meaning in a hover title; names, link names and the fields that the case writes
    itself are written out below, those in an accent. Below data, its text."""
    scale, left, h = 1.5, 76, 18
    right = left + BLOCK * scale
    out, y = [], 6
    for offset, data, what, details in archive.blocks:
        for k in range(0, len(data), BLOCK):
            block = data[k : k + BLOCK]
            label = what if k == 0 else f"{what.split(':')[0]}, continued"
            out.append(f'<text class="mono" x="4" y="{y + 11}">{offset + k:#08x}</text>'
                       f'<text x="{left}" y="{y + 11}">{esc(label)}</text>')
            y += 16
            if k == 0 and details and not isinstance(details[0], str):
                texts = []
                for field, start, w, raw, meaning, explicit in details:
                    x = left + start * scale
                    hover = f"{field} [{start},{start + w}): {show(raw)}" + (
                        f", {meaning}" if meaning else "")
                    out.append(f'<g><title>{esc(hover)}</title><rect class="field" x="{x:g}" '
                               f'y="{y}" width="{w * scale:g}" height="{h}"/>'
                               f"{runs(raw, x, y, scale, h)}</g>")
                    if w * scale >= 6 * len(field) + 4:
                        out.append(f'<text class="small" x="{x + w * scale / 2:g}" '
                                   f'y="{y + h + 11}">{esc(field)}</text>')
                    if explicit or (field in ("name", "linkname") and raw.strip(b"\0")):
                        texts.append((x, f"{field} {show(raw)}", "mono accent" if explicit
                                      else "mono"))
                for field, start, w, raw, meaning, explicit in details:
                    if explicit:
                        out.append(f'<rect class="mark" x="{left + start * scale - 1:g}" '
                                   f'y="{y - 1}" width="{w * scale + 2:g}" height="{h + 2}"/>')
                svg, y = callouts(texts, left, right, y + h + 14)
                out.append(svg)
            else:
                lines = [d for d in details if isinstance(d, str)]
                hover = "; ".join(lines) or "512 NUL"
                if len(data) > BLOCK:
                    hover = f"bytes {k} to {k + BLOCK} of {len(data)}: {hover}"
                out.append(f'<g><title>{esc(hover)}</title><rect class="field" x="{left}" '
                           f'y="{y}" width="{BLOCK * scale:g}" height="{h}"/>'
                           f"{runs(block, left, y, scale, h)}</g>")
                y += h + 4
                if k == 0:
                    for line in lines[1:]:
                        if len(line) > 116:
                            line = clip(line, 115)
                        out.append(f'<text class="mono" x="{left}" y="{y + 12}">{esc(line)}</text>')
                        y += 14
            y += 10
    out.append(f'<text class="mono" x="4" y="{y + 11}">{archive.size:#08x}</text>'
               f'<text x="{left}" y="{y + 11}">end of file</text>')
    y += 34
    x = left
    for cls, _, meaning in BYTE_CLASSES + [("mark", None, "written by the case itself")]:
        out.append(f'<rect class="field {cls}" x="{x}" y="{y - 10}" width="12" height="12"/>'
                   f'<text x="{x + 16}" y="{y}">{esc(meaning)}</text>')
        x += 16 + 6 * len(meaning) + 14
    width, height = max(right, x) + 8, y + 8
    colours = "".join(f".{c}{{fill:{colour}}}" for c, colour, _ in BYTE_CLASSES)
    style = (f"<style>text{{font-family:{FONT};font-size:12px;fill:#1f2328}}"
             ".mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;"
             "font-size:11px;fill:#59636e}.accent{fill:#bc4c00;font-weight:600}"
             ".small{font-size:10px;text-anchor:middle;fill:#59636e}"
             f".field{{fill:#ffffff;stroke:#59636e;stroke-width:0.75}}{colours}"
             ".mark{fill:none;stroke:#bc4c00;stroke-width:2}</style>"
             '<rect width="100%" height="100%" fill="#ffffff"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:g}" height="{height}" '
            f'viewBox="0 0 {width:g} {height}" role="img"><title>{esc(title)}</title>{style}'
            f'{"".join(out)}</svg>\n')
