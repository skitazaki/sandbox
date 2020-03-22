# -*- coding: utf-8 -*-

"""FizzBuzz impl.
"""

from sandboxlib import parse_args


def fizzbuzz(i):
    """Basic implementation."""
    if i % 15 == 0:
        print("FizzBuzz")
    elif i % 5 == 0:
        print("Buzz")
    elif i % 3 == 0:
        print("Fizz")
    else:
        print(i)


def fizzbuzz_iter(n):
    """Generator, using zip and postposion IF statement."""
    fb = ("Fizz", "Buzz")
    i = 1
    while i <= n:
        t = [i % 3 == 0, i % 5 == 0]
        s = ""
        for t1, t2 in zip(t, fb):
            if t1:
                s += t2
        yield s if s else i
        i += 1


def fizzbuzz_list(n):
    """map, filter and lamba function. also showing enumerate and type."""
    ret = []
    m0 = range(1, n + 1)
    m1 = map(lambda i: i if i % 3 > 0 else "Fizz", m0)
    m2 = map(lambda i: i if i % 5 > 0 else "Buzz", m0)
    m3 = map(lambda i: i if i % 15 > 0 else "FizzBuzz", m0)
    for i, t in enumerate(zip(m1, m2, m3)):
        r = list(filter(lambda s: type(s) is str, t))
        ret.append(r.pop() if r else f"{i + 1}")
    return ret


def setup_arguments(parser):
    parser.add_argument("number", nargs=1, type=int, help="positive integer")


def main():
    args = parse_args(doc=__doc__, prehook=setup_arguments)
    n = args.number[0]

    if n <= 0:
        raise SystemError("Invalid input, positive NUMBER is required.")

    print("=" * 78)
    for i in range(1, n + 1):
        fizzbuzz(i)

    print("=" * 78)
    for i in fizzbuzz_iter(n):
        print(i)

    print("=" * 78)
    print("\n".join(fizzbuzz_list(n)))


def test():
    expected = [
        "1",
        "2",
        "Fizz",
        "4",
        "Buzz",
        "Fizz",
        "7",
        "8",
        "Fizz",
        "Buzz",
        "11",
        "Fizz",
        "13",
        "14",
        "FizzBuzz",
        "16",
    ]
    actual = fizzbuzz_list(16)
    assert len(expected) == len(actual)
    for e, a in zip(expected, actual):
        assert e == a


if __name__ == "__main__":
    main()
