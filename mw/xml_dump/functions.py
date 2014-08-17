import os
import re
import subprocess

from .errors import FileTypeError

EXTENSIONS = {
    'xml': ["cat"],
    'gz': ["zcat"],
    'bz2': ["bzcat"],
    '7z': ["7z", "e", "-so"],
    'lzma': ["lzcat"]
}
"""
A map from file extension to the command to run to extract the data to standard out.
"""

EXT_RE = re.compile(r'\.([^\.]+)$')
"""
A regular expression for extracting the final extension of a file.
"""


def file(path_or_f):
    """
    Verifies that a file exists at a given path and that the file has a
    known extension type.

    :Parameters:
        path : `str`
            the path to a dump file

    """
    if hasattr(path_or_f, "readline"):
        return path_or_f
    else:
        path = path_or_f

    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        raise FileTypeError("Can't find file %s" % path)

    match = EXT_RE.search(path)
    if match is None:
        raise FileTypeError("No extension found for %s." % path)
    elif match.groups()[0] not in EXTENSIONS:
        raise FileTypeError("File type %r is not supported." % path)
    else:
        return path


def open_file(path_or_f):
    """
    Turns a path to a dump file into a file-like object of (decompressed)
    XML data.

    :Parameters:
        path : `str`
            the path to the dump file to read
    """
    if hasattr(path_or_f, "read"):
        return path_or_f
    else:
        path = path_or_f

    match = EXT_RE.search(path)
    ext = match.groups()[0]
    p = subprocess.Popen(
        EXTENSIONS[ext] + [path],
        stdout=subprocess.PIPE,
        stderr=open(os.devnull, "w")
    )
    # sys.stderr.write("\n%s %s\n" % (EXTENSIONS[ext], path))
    # sys.stderr.write(p.stdout.read(1000))
    # return False
    return p.stdout
