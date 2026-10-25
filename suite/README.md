# The test suite

Tar archives, each with a verdict, and unless it is to reject, the tree that an implementation
must extract from it. [METHOD.md](../METHOD.md#verdicts) explains the verdicts, and
[the site](https://stoppels.ch/tar/) has a page per case, with its blocks and
what implementations make of it.

**Some archives escape the directory they are extracted to in lenient implementations.** Their
files are harmless, and say in their names and contents what happened, but extract them in a
throwaway directory.

## Using it

Every case is an uncompressed archive, `archives/<case>.tar`, with its manifest
`archives/<case>.json` next to it:

```json
{
 "id": "N07",
 "verdict": "tolerate",
 "description": "A symlink to an absolute path, created as it is.",
 "features": ["symlink.absolute"],
 "tree": [{"path": "link", "kind": "symlink", "target": "/tar-minefield-nonexistent"}]
}
```

- `verdict`: `reject`, a strict parser must reject the archive; `accept`, every implementation
  must extract `tree` from it; `tolerate`, a strict parser may reject it, and must extract `tree`
  if it does not.
- `tree`: every path the archive extracts to, directories included, each with its `kind`
  (`file`, `directory` or `symlink`), the `target` of a symlink, and of a file its `size`,
  `sha256` and whether it is `executable`. An extraction passes if it has exactly these paths,
  and every entry has the values the manifest gives. It is absent from the cases to reject.
- `id`: the case's identifier, such as `N07`, which stays with it. Its letter is the category: F
  framing, N names, K kinds, S order and state.
- `features`: what [the scanner](../contrib/scanner) reports of the archive, for reference.

The suite needs nothing but the archives and their manifests: copy `archives/`, or this
directory, into the tests of an implementation.

## Layout

- `archives/<case>.tar`: the archive, uncompressed.
- `archives/<case>.json`: its manifest, as above.
- `archives/<case>.txt`: what the case is about, and every block of the archive with its offset
  and, for headers, every field with its raw bytes.
- `archives/<case>.svg`: a map of its blocks, every one 512 bytes to scale, with the fields of
  headers where they are, and the bytes that the case writes itself marked.
- `cases/<case>.py`: the script that writes it, whose docstring explains the case: the decision
  point where implementations differ, where the scans saw it, and what implementations do with it.
- `blocks.py`: writes archives from raw 512-byte blocks, and describes each block as it writes
  it. It does not use a tar implementation, so that the test suite does not test one against
  itself.

## Generating and checking

```console
$ python -I suite/generate.py            # write archives/
$ python -I suite/generate.py --check    # fail if archives/ is not what the scripts write
```

Generation is deterministic, with the Python standard library only.
[contrib/scanner](../contrib/scanner) checks the scanner and the default policy against the
cases.

A new case is a script in `cases/`, named by its identifier and a few words, with `ID`, `VERDICT`
(`"reject"`, `"accept"` or `"tolerate"`), `FEATURES`, `TREE` unless it is to reject, and a
`build(archive)` function. Its identifier is the next free number of its letter.
