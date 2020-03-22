# -*- coding: utf-8 -*-

"""Use "inspect" module.
"""

import inspect


def func1():
    """Function No.1.
    do nothing special.
    """
    print(__doc__)


def func2():
    """Function No.2.
    of course, do nothing special, too.
    """
    print(__file__)


FUNCTIONS = [func1, func2]


def main():
    for f in FUNCTIONS:
        print("-" * 78)
        print(f"--> {f.__name__} <--")
        print(f"{f} defined in {inspect.getfile(f)}")
        print(f"Arguments: {inspect.signature(f)}")
        print(inspect.getdoc(f))
        print("Invoke!!")
        f()


if __name__ == "__main__":
    main()
