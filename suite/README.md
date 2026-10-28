# The test suite

Tar archives, each with a verdict, and unless it is to reject, the tree that an implementation
must extract from it. [METHOD.md](../METHOD.md#verdicts) explains the verdicts, and
[the site](https://stoppels.ch/tar/) has a page per case.

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

Tests of a library can read the cases themselves. Every case is an archive,
`archives/<case>.tar`, such as `archives/N07-symlink-absolute.tar`, with its expected result in
`archives/<case>.json`:

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
- `features`: what [the scanner](../contrib/scanner) reports of the archive, for reference.

Copy `archives/`, or this directory to have `check.py` too, into the tests of an implementation.

## Layout

- `archives/<case>.txt`: every block of the archive, with its offset and, for headers, every
  field with its raw bytes.
- `archives/<case>.svg`: a map of the blocks, every one 512 bytes to scale.
- `cases/<case>.py`: the script that writes the case, whose docstring explains it.
- `blocks.py`: writes archives from raw 512-byte blocks, without a tar implementation, so that
  the suite does not test one against itself.
- `generate.py`: writes `archives/` from the scripts, deterministically, or with `--check` fails
  if `archives/` is not what they write.

A new case is a script in `cases/`, named by its identifier, the next free number of its letter,
and a few words. The scripts there show what it defines.
