from mk.core import eq, Var
from mk.ext import conde, zzz
from mk.arithmetic import add, sub, mul, div
from mk.constraints import make_predicate
from mk.run import run


is_int = make_predicate(lambda a: isinstance(a, int))


def calc(e, o):
    a, b = Var(), Var()
    ca, cb = Var(), Var()
    op = Var()
    return conde(
        [
            eq((op, a, b), e),
            zzz(lambda: calc(a, ca)),
            zzz(lambda: calc(b, cb)),
            conde(
                [eq("+", op), add(ca, cb, o)],
                [eq("-", op), sub(ca, cb, o)],
                [eq("*", op), mul(ca, cb, o)],
                [eq("/", op), div(ca, cb, o)],
            )
        ],
        [is_int(e), eq(e, o)]
    )


def main():
    expr = ("/", ("+", 4, ("*", 2, ("-", 8, 5))), 2)
    out = Var()
    for s in run(0, out, calc(expr, out)):
        print(s)


if __name__ == '__main__':
    main()
