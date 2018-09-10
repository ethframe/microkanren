from mk.core import eq, eqt, disj, conj, Var
from mk.run import run
from mk.ext import disjp, conjp, conde, fresh, zzz
from mk.disequality import neq
from mk.list import pair_to_list


def lookup(x, env, t):
    return fresh(lambda rest, y, v: conj(
        eq(((y, v), rest), env),
        conde(
            [eq(y, x), eq(v, t)],
            [neq(y, x), zzz(lambda: lookup(x, rest, t))]
        )
    ))


def missing(x, env):
    return disj(
        eq((), env),
        fresh(lambda rest, y, v: conjp(
            eq(((y, v), rest), env),
            neq(y, x),
            zzz(lambda: missing(x, rest))
        ))
    )


def proper(exp, env, val):
    return conde(
        [eq((), exp), eq((), val)],
        [
            fresh(lambda a, d, ta, td: conjp(
                eq((a, d), exp),
                eq((ta, td), val),
                zzz(lambda: eval_exp(a, env, ta)),
                zzz(lambda: proper(d, env, td))
            ))
        ]
    )


def eval_exp(exp, env, val):
    return disjp(
        fresh(lambda v: conjp(
            eq(("quote", (v, ())), exp),
            missing("quote", env),
            eq(v, val),
        )),
        fresh(lambda ap: conjp(
            eq(("list", ap), exp),
            missing("list", env),
            proper(ap, env, val),
        )),
        conjp(
            eqt(exp, str),
            lookup(exp, env, val),
        ),
        fresh(lambda rator, rand, x, body, envc, a: conjp(
            eq((rator, (rand, ())), exp),
            zzz(lambda: eval_exp(rator, env, ("closure", x, body, envc))),
            zzz(lambda: eval_exp(rand, env, a)),
            zzz(lambda: eval_exp(body, ((x, a), envc), val))
        )),
        fresh(lambda x, body: conjp(
            eq(("lambda", ((x, ()), (body, ()))), exp),
            eqt(x, str),
            missing("lambda", env),
            eq(("closure", x, body, env), val)
        ))
    )


def main():
    q = Var()
    for s in run(5, q, eval_exp(q, (), q)):
        print(pair_to_list(s, True))


if __name__ == '__main__':
    main()
