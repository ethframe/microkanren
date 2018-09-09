from mk.arithmetic import add, gte, lte
from mk.disequality import neq
from mk.unify import Var
from mk.core import conj, disj, eq
from mk.ext import call_fresh, conde, conjp, fresh, run, zzz
from mk.list import pair_to_list


def jugs(states):
    return disj(
        eq(((0, 0, ""), ()), states),
        fresh(lambda big, small, act, prev_big, prev_small, tail, _, __: conjp(
            eq(((big, small, act), tail), states),
            eq(((prev_big, prev_small, _), __), tail),
            zzz(lambda: jugs(tail)),
            conde(
                [
                    conde(
                        [
                            conde(
                                [eq(big, 5), eq(act, "fill big")],
                                [eq(big, 0), eq(act, "empty big")]),
                            eq(small, prev_small)],
                        [
                            call_fresh(
                                lambda total: conjp(
                                    add(big, small, total),
                                    add(prev_big, prev_small, total),
                                    conde(
                                        [eq(big, 5), eq(act, "to big")],
                                        [eq(small, 3), eq(act, "to small")],
                                        [
                                            eq(small, 0), neq(big, 5),
                                            eq(act, "to big")],
                                        [
                                            eq(big, 0), neq(small, 3),
                                            eq(act, "to small")])))]),
                    neq(big, prev_big)],
                [
                    conde(
                        [eq(small, 3), eq(act, "fill small")],
                        [eq(small, 0), eq(act, "empty small")]),
                    neq(small, prev_small), eq(big, prev_big)]),
            gte(big, 0), lte(big, 5),
            gte(small, 0), lte(small, 3)
        )))


def main():
    states = Var()
    big = Var()
    small = Var()
    _ = Var()
    __ = Var()
    for i in range(1, 6):
        p = conjp(
            eq(((big, small, _), __), states),
            disj(
                eq(big, i),
                conj(neq(big, i), eq(small, i)),
            ),
            jugs(states)
        )
        for answer in run(1, states, p):
            print("{}:".format(i))
            for b, s, a in reversed(list(pair_to_list(answer))):
                print(b, s, a)
            print()


if __name__ == '__main__':
    main()
