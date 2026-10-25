<?php
// Extract a tar archive with ext/phar's PharData, as Composer's TarDownloader calls it, for
// contrib/matrix/matrix.py.
//
//     php extract.php ARCHIVE DEST
//
// An error is printed on stderr, with status 1.
[, $archive, $dest] = $argv;
try {
    (new PharData($archive))->extractTo($dest, null, true);
} catch (Exception $e) {
    fwrite(STDERR, get_class($e) . ': ' . $e->getMessage() . "\n");
    exit(1);
}
