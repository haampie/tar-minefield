"""An ACL in a pax header that gives the owner of a file the execute permission.

The archive has a file `a` with the mode 644, whose pax header has the record
`SCHILY.acl.access=user::rwx,group::r-x,other::r-x`.

The key `SCHILY.acl.access` is star's, for the access control list of a file, and libarchive and GNU
tar write it too. The entries `user::`, `group::` and `other::` of such a list are the permissions
of the owner, the group and others, which are also in the mode. A writer stores both as they are on
the file system, where they agree. Here they do not: the mode is 644, and the list says 755. This
case is ambiguous because a reader that does not restore ACLs extracts `a` with the mode 644, and
one that does makes `a` executable.

Decision point: whether an ACL in a pax header is applied.
Seen in: not measured, as the scans record the 8 most common pax keys of a tarball, and of xattrs
not their names: a key `SCHILY.acl.*` is not among those of any tarball, and at most 45 of the
scanned tarballs have xattrs, in which Linux keeps ACLs, or more keys.
See also: K09, an executable file, and F31, an xattr in a pax header.
"""

VERDICT = "reject"
ID = "K12"
FEATURES = ["pax.acl"]


def build(a):
    a.pax([(b"SCHILY.acl.access", b"user::rwx,group::r-x,other::r-x")],
          note="an ACL that says 755")
    a.file(b"a", b"a\n")
    a.end()
