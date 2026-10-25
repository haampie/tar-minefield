"""The sentences of POSIX that the cases rely on, and links to them: to their section of the pax
utility in POSIX.1-2024, with a text fragment that highlights the sentence, so that a browser
without text fragments still shows the section.

A case names its sentence as `POSIX = "<key>"`, next to its FEATURES, and the site links the first
"POSIX" of its explanation to it. Checked against the page as it is published, that every sentence
is in its section, once, and so are the ones that METHOD.md links to:

    python -I contrib/citations.py
"""

import html
import os
import re
import sys
import urllib.parse
import urllib.request

PAGE = "https://pubs.opengroup.org/onlinepubs/9799919799/utilities/pax.html"
# The sections, by their ids on the page
END = "tag_20_94_13_01"  # pax Interchange Format
PAX_HEADER = "tag_20_94_13_02"  # pax Header Block
PAX_EXTENDED = "tag_20_94_13_03"  # pax Extended Header
PRECEDENCE = "tag_20_94_13_04"  # pax Extended Header Keyword Precedence
USTAR = "tag_20_94_13_06"  # ustar Interchange Format
SENTENCES = {
    "end": (END, "there shall be two 512-byte blocks filled with binary zeros"),
    "version": (USTAR, 'The version field is two octets containing the characters "00"'),
    "checksum": (USTAR, "Each octet in the header shall be treated as an unsigned value"),
    "numeric": (USTAR, "Each numeric field is terminated by one or more <space> or NUL characters"),
    "record-length": (PAX_EXTENDED, "The <length> field shall be the decimal length of the extended "
                                    "header record in octets"),
    "size-override": (PAX_EXTENDED, "This record shall override the size field in the following "
                                    "header block(s)"),
    "no-data": (USTAR, "No data logical records are stored for types 1, 2, or 5"),
    "unknown-type": (USTAR, "the file shall be extracted as if it were a regular file"),
    "extended": (PAX_HEADER, "Represents extended header records for the following file in the "
                             "archive"),
    "global": (PAX_HEADER, "Each value shall affect all subsequent files that do not override that "
                           "value"),
    "empty-value": (PAX_EXTENDED, "If the <value> field is zero length, it shall delete any header "
                                  "block field"),
    "size-decimal": (PAX_EXTENDED, "The size of the file in octets, expressed as a decimal number"),
    "comment": (PAX_EXTENDED, "All characters in the <value> field shall be ignored by pax"),
    "utf-8": (PAX_EXTENDED, "The extended header records shall be encoded according to the "
                            "ISO/IEC 10646-1:2020 standard UTF-8 encoding"),
    "hdrcharset": (PAX_EXTENDED, "values recorded in extended headers for affected files are "
                                 "unencoded binary data"),
    "linkname": (USTAR, "The linked-to name is specified in the linkname field"),
    "last-wins": (PRECEDENCE, "When extended header records conflict, the last one given in the "
                              "header shall take precedence"),
    "name-nul": (USTAR, "name is terminated at the first NUL character"),
    "invalid-name": (USTAR, "invalid filename, it is implementation-defined whether the data from "
                            "the file is stored on the file hierarchy"),
    "hardlink": (USTAR, "Represents a file linked to another file, of any type, previously "
                        "archived"),
}


def link(section, sentence):
    # a dash, comma or ampersand is syntax in a text directive, so they are escaped too
    text = urllib.parse.quote(sentence, safe="").replace("-", "%2D")
    return f"{PAGE}#{section}:~:text={text}"


def url(key):
    return link(*SENTENCES[key])


# The tags after which a browser starts a new line: a text fragment matches across the others
BLOCK = r"</?(p|h\d|td|th|tr|li|dt|dd|dl|ul|ol|br|pre|div|blockquote|table|center|hr)\b[^>]*>"


def text(page):
    """The text of the page, near enough as a browser lays it out."""
    page = re.sub(BLOCK, " ", page, flags=re.I)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", "", page)).split())


def main():
    with urllib.request.urlopen(PAGE) as f:
        page = f.read().decode("latin-1")
    starts = [(len(text(page[:m.start()])), m.group(1))
              for m in re.finditer(r'id="(tag_[0-9_]+)"', page)]
    whole = text(page)
    with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "METHOD.md")) as f:
        method = f.read()
    cited = list(SENTENCES.items())
    for section, fragment in re.findall(re.escape(PAGE) + r"#(\w+):~:text=([^)\s]+)", method):
        cited.append(("METHOD.md", (section, urllib.parse.unquote(fragment))))
    problems = []
    for key, (section, sentence) in cited:
        at = [m.start() for m in re.finditer(re.escape(sentence), whole, re.I)]
        if len(at) != 1:
            problems.append(f"{key}: {len(at)} times on the page: {sentence}")
        elif max(s for s in starts if s[0] <= at[0])[1] != section:
            problems.append(f"{key}: not in {section}: {sentence}")
    if problems:
        sys.exit("\n".join(problems))


if __name__ == "__main__":
    main()
