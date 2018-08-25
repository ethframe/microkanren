from .core import eq, disj, conj
from .ext import call_fresh, fresh, disjp, conjp, conde, condp, zzz
from .list import list_to_pair, pair_to_list


def int_to_pair(n):
    bits = []
    while n:
        bits.append(n % 2)
        n //= 2
    return list_to_pair(bits)


def pair_to_int(pair):
    bits = pair_to_list(pair)
    n = 0
    for i in reversed(bits):
        n = n * 2 + i
    return n


def zero(v):
    return eq(v, ())


def pos(v):
    return fresh(lambda a, b: eq(v, (a, b)))


def gt1(v):
    return fresh(lambda a, b, c: eq(v, (a, (b, c))))


def genb(v):
    return disjp(
        zero(v),
        call_fresh(
            lambda X: conj(eq(v, (0, X)), zzz(lambda: conj(pos(X), genb(X))))
        ),
        call_fresh(
            lambda X: conj(eq(v, (1, X)), zzz(lambda: genb(X)))
        ),
    )


def lessl(a, b):
    return disj(
        conj(zero(a), pos(b)),
        fresh(
            lambda x, X, y, Y: conjp(
                eq(a, (x, X)),
                eq(b, (y, Y)),
                zzz(lambda: lessl(X, Y))
            )
        )
    )


def full1_adder(cin, a, b, s, cout):
    return condp(
        (cin, a, b, s, cout),
        [(0, 0, 0, 0, 0)],
        [(0, 0, 1, 1, 0)],
        [(0, 1, 0, 1, 0)],
        [(0, 1, 1, 0, 1)],
        [(1, 0, 0, 1, 0)],
        [(1, 0, 1, 0, 1)],
        [(1, 1, 0, 0, 1)],
        [(1, 1, 1, 1, 1)],
    )


def fulln_adder(cin, a, b, s):
    return disjp(
        conj(
            eq(cin, 0),
            conde(
                [eq(b, ()), eq(s, a)],
                [eq(a, ()), eq(s, b), pos(b)],
            )
        ),
        conjp(
            eq(cin, 1),
            conde(
                [eq(b, ()), zzz(lambda: fulln_adder(0, a, (1, ()), s))],
                [eq(a, ()), zzz(lambda: fulln_adder(0, (1, ()), b, s))],
            )
        ),

        conj(
            eq(a, (1, ())),
            disj(
                conj(
                    eq(b, (1, ())),
                    fresh(
                        lambda r1, r2: conj(
                            full1_adder(cin, 1, 1, r1, r2),
                            eq(s, (r1, (r2, ()))),
                        )
                    ),
                ),
                fresh(
                    lambda bb, br, rb, rr, cout: conjp(
                        eq(b, (bb, br)),
                        eq(s, (rb, rr)),
                        pos(br), pos(rr),
                        full1_adder(cin, 1, bb, rb, cout),
                        zzz(lambda: fulln_adder(cout, (), br, rr))
                    )
                ),
            )
        ),
        conjp(
            eq(b, (1, ())),
            gt1(a), gt1(s),
            zzz(lambda: fulln_adder(cin, (1, ()), a, s)),
        ),

        fresh(
            lambda ab, ar, bb, br, rb, rr, cout: conjp(
                eq(a, (ab, ar)),
                eq(b, (bb, br)),
                eq(s, (rb, rr)),
                pos(ar), pos(br), pos(rr),
                full1_adder(cin, ab, bb, rb, cout),
                zzz(lambda: fulln_adder(cout, ar, br, rr))
            )
        )
    )


def add(a, b, c):
    return fulln_adder(0, a, b, c)


def sub(a, b, c):
    return add(b, c, a)


def less(a, b):
    return fresh(lambda X: conj(pos(X), add(a, X, b)))


def mul(n, m, p):
    return disjp(
        conj(eq(n, ()), eq(p, ())),
        conjp(eq(m, ()), eq(p, ()), pos(n)),

        conjp(eq(n, (1, ())), eq(p, m), pos(m)),

        fresh(
            lambda nr, pr: conjp(
                eq(n, (0, nr)), eq(p, (0, pr)),
                pos(m), pos(nr), pos(pr),
                zzz(lambda: mul(nr, m, pr))
            )
        ),

        fresh(
            lambda nr, p1: conjp(
                eq(n, (1, nr)),
                pos(m), pos(nr), gt1(p),
                lessl3(p1, p, (1, nr), m),
                zzz(lambda: mul(nr, m, p1)),
                add((0, p1), m, p)
            )
        )
    )


def lessl3(p1, p, n, m):
    return disjp(
        conjp(eq(p1, ()), fresh(lambda a, b: eq(p, (a, b)))),
        conj(
            eq(n, ()),
            fresh(
                lambda p1b, p1r, pb, pr, mb, mr: conjp(
                    eq(p1, (p1b, p1r)),
                    eq(p, (pb, pr)),
                    eq(m, (mb, mr)),
                    zzz(lambda: lessl3(p1r, pr, (), mr))
                )
            )
        ),
        fresh(
            lambda p1b, p1r, pb, pr, nb, nr: conjp(
                eq(p1, (p1b, p1r)),
                eq(p, (pb, pr)),
                eq(n, (nb, nr)),
                zzz(lambda: lessl3(p1r, pr, nr, m))
            )
        )
    )
