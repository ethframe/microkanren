from mk.arithmetic import add, gte, lte
from mk.core import conj, disj, eq
from mk.disequality import neq
from mk.ext import conde, conjp, delay, fresh, run
from mk.unify import Var

# BIG = 5
# SMALL = 3


BIG = 9
SMALL = 4


@delay
def jugs(states):
    return disj(
        eq([(0, 0, "")], states),
        fresh[8](
            lambda big, small, act, prev_big, prev_small, tail, _, __: conjp(
                eq([(big, small, act), tail, ...], states),
                eq([(prev_big, prev_small, _), __, ...], tail),
                conde(
                    [
                        conde(
                            [
                                eq(small, prev_small),
                                conde(
                                    [eq(big, BIG), eq(act, "fill big")],
                                    [eq(big, 0), eq(act, "empty big")])],
                            [
                                fresh(
                                    lambda total: conjp(
                                        conde(
                                            [eq(big, BIG), eq(act, "to big")],
                                            [
                                                eq(small, SMALL),
                                                eq(act, "to small")],
                                            [
                                                eq(small, 0), neq(big, BIG),
                                                eq(act, "to big")],
                                            [
                                                eq(big, 0), neq(small, SMALL),
                                                eq(act, "to small")]),
                                        add(big, small, total),
                                        add(prev_big, prev_small, total)))]),
                        neq(big, prev_big)],
                    [
                        eq(big, prev_big),
                        conde(
                            [eq(small, SMALL), eq(act, "fill small")],
                            [eq(small, 0), eq(act, "empty small")]),
                        neq(small, prev_small)]),
                gte(big, 0), lte(big, BIG),
                gte(small, 0), lte(small, SMALL),
                jugs(tail),
            )))


def main():
    states = Var()
    big = Var()
    small = Var()
    _ = Var()
    __ = Var()
    for i in range(1, BIG + 1):
        p = conjp(
            eq([(big, small, _), __, ...], states),
            disj(
                eq(big, i),
                conj(neq(big, i), eq(small, i)),
            ),
            jugs(states)
        )
        for answer in run(1, states, p):
            print("{}:".format(i))
            for b, s, a in reversed(answer):
                print(b, s, a)
            print()


if __name__ == '__main__':
    main()
