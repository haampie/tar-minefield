"""A pax ACL record that grants owner execute permission on a mode-644 file.

The archive has a file `a` with mode 644 in its ustar header and
`SCHILY.acl.access=user::rwx,group::r-x,other::r-x` in its pax header.

Star introduced `SCHILY.acl.access` for POSIX access control lists, and libarchive and GNU tar use
it as well. Its `user::`, `group::` and `other::` entries mirror the traditional owner, group and
other mode bits. Normal archivers write consistent permissions in both places, whereas this archive
pairs a ustar mode of 644 with an ACL equivalent to 755. A reader that ignores ACLs leaves `a` at
mode 644, while one that applies the ACL makes `a` executable.

Decision point: whether a pax ACL record is applied on extraction.
Seen in: not measured, as the scanner records only the 8 most common pax keys per tarball and does
not record xattr names; no tarball has `SCHILY.acl.*` among its top 8 keys, and 45 scanned tarballs
have additional keys or xattrs where an ACL could live.
See also: K09, an executable file, and F31, an xattr in a pax header.
"""

VERDICT = "reject"
ID = "K12"
FEATURES = ["pax.acl"]


def build(a):
    a.pax([(b"SCHILY.acl.access", b"user::rwx,group::r-x,other::r-x")],
          note="ACL granting mode 755")
    a.file(b"a", b"a\n")
    a.end()
