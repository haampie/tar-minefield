# The test suite

Each case is a tar archive with a verdict: to reject, to accept, or tolerated. Unless the verdict
is to reject, the case also gives the tree that an implementation must extract from the archive.
[METHOD.md](../METHOD.md#verdicts) explains the verdicts, and [the site](https://stoppels.ch/tar/)
explains each case in detail.

**Some archives escape the directory they are extracted to in lenient implementations.** Their
files are harmless, and say in their names and contents what happened, but extract them in a
throwaway directory.

## Using it

To check an extractor, run `check.py` with the command that extracts one archive:

```console
$ python -I suite/check.py -- tar -xf '{archive}' -C '{dest}'
```

It extracts every case in a temporary directory of its own, and says which cases fail, and what
the extractor wrote outside the directory.

If your project does not expose a command line utility, it is best to write your own tests. It is
allowed to copy the test cases over.

Every case is an archive, `archives/<case>.tar`, such as `archives/N07-symlink-absolute.tar`, with
its expected result in `archives/<case>.json`:

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
  and every entry has the values that `tree` gives. It is absent from the cases to reject.
- `id`: the identifier, which stays with the case. Its letter is the category: F framing, N
  names, K kinds, S order and state.
- `features`: labels of what the case is about, such as `symlink.absolute`, for reference.
