# -*- coding: utf-8 -*-

"""Check I/O encoding, see Appendix 1.2 of Expert Python Programming.
"""

import locale
import sys


def main():
    patterns = [
        ("stdin", sys.stdin),
        ("stdout", sys.stdout),
        ("stderr", sys.stderr),
    ]
    for label, descriptor in patterns:
        print(f"{label}: {descriptor.fileno()=} {descriptor.encoding=}")
    print(f"preferred locale: {locale.getpreferredencoding()}")
    print(f"file system: {sys.getfilesystemencoding()}")


if __name__ == "__main__":
    main()
