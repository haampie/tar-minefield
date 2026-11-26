"""An absolute name, which points outside the directory the archive is extracted to.

The archive has one file, `/tmp/tar-minefield-absolute`, with a leading slash.

The case is rejected because the name, taken as it is, leads out of the destination, not because it
is ambiguous. In [POSIX][resolution], files are created by pathname resolution, which follows an
absolute path outside the destination directory. The test payload targets `/tmp` with harmless text
so that an extractor that follows the name can write it without root privileges.

Decision point: whether an absolute name is rejected, made relative, or followed.
Seen in: dtv-scan-tables (`/usr/share/dvb/`) and masurca 3.3.1.
"""

VERDICT = "reject"
ID = "N12"
FEATURES = ['name.absolute']


def build(a):
    a.file(b"/tmp/tar-minefield-absolute", b"If this file is outside the directory you extracted to, the extractor followed the name.\n")
    a.end()
