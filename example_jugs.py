from mk.core import Var, eq, disj, conj
from mk.ext import call_fresh, fresh, conjp, conde, zzz, runp
from mk.list import pair_to_list
from mk.arithmetic import add, pos, less, int_to_pair, pair_to_int


zero = ()
one = int_to_pair(1)
two = int_to_pair(2)
three = int_to_pair(3)
four = int_to_pair(4)
five = int_to_pair(5)
six = int_to_pair(6)


def neqo(a, b):
    return call_fresh(
        lambda X: conj(
            disj(add(a, X, b), add(b, X, a)),
            pos(X)))


def jugso(A):
    return disj(
        eq(((zero, zero), ()), A),
        fresh(lambda B, S, PB, PS, T, PT: conjp(
            eq(((B, S), T), A),
            zzz(lambda: jugso(T)),
            less(B, six),
            less(S, four),
            eq(((PB, PS), PT), T),
            conde(
                [
                    neqo(B, PB),
                    conde(
                        [disj(eq(B, five), eq(B, zero)), eq(S, PS)],
                        [
                            call_fresh(
                                lambda R: conjp(
                                    add(B, S, R), add(PB, PS, R),
                                    conde(
                                        [eq(B, five)],
                                        [eq(S, three)],
                                        [eq(S, zero), neqo(B, five)],
                                        [eq(B, zero), neqo(S, three)])))])],
                [disj(eq(S, zero), eq(S, three)), neqo(S, PS), eq(B, PB)]))))


def main():
    a = Var()
    t = Var()
    for s in runp(1, a, eq(((four, ()), t), a), jugso(a)):
        for a, b in reversed(pair_to_list(s)):
            print(pair_to_int(a), pair_to_int(b))


if __name__ == '__main__':
    main()
