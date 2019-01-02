from mk.arithmetic import add, div, mul, sub
from mk.core import eq, eqt
from mk.dsl import conde, delay
from mk.run import run
from mk.unify import Var


@delay
def calc(e, o):
    a, b = Var(), Var()
    ca, cb = Var(), Var()
    op = Var()
    return conde(
        [
            eq((op, a, b), e),
            calc(a, ca),
            calc(b, cb),
            conde(
                [eq("+", op), add(ca, cb, o)],
                [eq("-", op), sub(ca, cb, o)],
                [eq("*", op), mul(ca, cb, o)],
                [eq("/", op), div(ca, cb, o)],
            )
        ],
        [eqt(e, int), eq(e, o)]
    )


def main():
    expr = ("/", ("+", 4, ("*", 2, ("-", 8, 5))), 2)
    out = Var()
    for s in run(0, out, calc(expr, out)):
        print(s)


if __name__ == '__main__':
    main()
