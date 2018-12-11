from mk.core import conj, disj, eq, eqt
from mk.disequality import neq
from mk.ext import conde, conjp, delay, disjp, fresh
from mk.run import run
from mk.unify import Var


class Symbol(str):
    def __repr__(self):
        return self

    def __eq__(self, other):
        return type(self) is type(other) and super().__eq__(other)


closure = object()


@delay
def lookup(x, env, t):
    return fresh(lambda rest, y, v: conj(
        eq(((y, v), rest), env),
        conde(
            [eq(y, x), eq(v, t)],
            [neq(y, x), lookup(x, rest, t)]
        )
    ))


@delay
def missing(x, env):
    return disj(
        eq((), env),
        fresh(lambda rest, y, v: conjp(
            eq(((y, v), rest), env),
            neq(y, x),
            missing(x, rest)
        ))
    )


@delay
def proper(exp, env, val):
    return conde(
        [eq([], exp), eq([], val)],
        [
            fresh(lambda a, d, ta, td: conjp(
                eq([a, d, ...], exp),
                eq([ta, td, ...], val),
                eval_exp(a, env, ta),
                proper(d, env, td)
            ))
        ]
    )


@delay
def eval_exp(exp, env, val):
    return disjp(
        fresh(lambda v: conjp(
            eq([Symbol("quote"), v], exp),
            missing(Symbol("quote"), env),
            eq(v, val),
        )),
        fresh(lambda ap: conjp(
            eq([Symbol("list"), ap, ...], exp),
            missing(Symbol("list"), env),
            proper(ap, env, val),
        )),
        conj(
            eqt(exp, Symbol),
            lookup(exp, env, val),
        ),
        fresh(lambda rator, rand, x, body, envc, a: conjp(
            eq([rator, rand], exp),
            eval_exp(rator, env, (closure, x, body, envc)),
            eval_exp(rand, env, a),
            eval_exp(body, ((x, a), envc), val)
        )),
        fresh(lambda x, body: conjp(
            eq([Symbol("lambda"), [x], body], exp),
            eqt(x, Symbol),
            missing(Symbol("lambda"), env),
            eq((closure, x, body, env), val)
        ))
    )


def format_sexpr(s):
    if isinstance(s, list):
        if len(s) == 2 and s[0] == Symbol("quote"):
            return "'" + format_sexpr(s[1])
        return "({})".format(" ".join(format_sexpr(e) for e in s))
    return repr(s)


def main():
    q = Var()
    for s in run(5, q, eval_exp(q, (), q)):
        print(format_sexpr(s))


if __name__ == '__main__':
    main()
