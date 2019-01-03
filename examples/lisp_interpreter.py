from collections import namedtuple

from mk.core import conj, disj, eq, eqt
from mk.disequality import neq
from mk.dsl import conde, conjp, delay, fresh
from mk.ext.lists import no_item
from mk.run import run
from mk.unify import Var


class Symbol(str):
    def __repr__(self):
        return self

    def __eq__(self, other):
        return type(self) is type(other) and super().__eq__(other)


Closure = namedtuple("Closure", "arg, body, env")
Env = namedtuple("Env", "var, val, env")


@delay
def lookup(var, env, out):
    return fresh(3, lambda rest, sym, val: conj(
        eq(Env(sym, val, rest), env),
        conde(
            (eq(sym, var), eq(val, out)),
            (neq(sym, var), lookup(var, rest, out))
        )
    ))


@delay
def missing(var, env):
    return disj(
        eq((), env),
        fresh(3, lambda rest, sym, val: conjp(
            eq(Env(sym, val, rest), env), neq(sym, var),
            missing(var, rest),
        )),
    )


@delay
def eval_list(lst, env, out):
    return conde(
        (eq([], lst), eq([], out)),
        fresh(4, lambda h, t, oh, ot: conjp(
            eq([h, t, ...], lst), eq([oh, ot, ...], out),
            eval_expr(h, env, oh), eval_list(t, env, ot),
        ))
    )


quote, list_, lambda_ = map(Symbol, "quote list lambda".split())


def is_closure(a):
    return type(a) is Closure


@delay
def eval_expr(exp, env, out):
    return conde(
        (eq([quote, out], exp), no_item(out, is_closure), missing(quote, env)),
        fresh(lambda lst: conjp(
            eq([list_, lst, ...], exp),
            missing(list_, env), eval_list(lst, env, out),
        )),
        fresh(4, lambda var, body, cenv, arg: conjp(
            eval_list(exp, env, [Closure(var, body, cenv), arg]),
            eval_expr(body, Env(var, arg, cenv), out),
        )),
        fresh(2, lambda var, body: conjp(
            eq([lambda_, [var], body], exp), eq(Closure(var, body, env), out),
            eqt(var, Symbol), missing(lambda_, env),
        )),
        (eqt(exp, Symbol), lookup(exp, env, out)),
    )


def format_sexpr(s):
    if isinstance(s, list):
        if len(s) == 2 and s[0] == Symbol("quote"):
            return "'" + format_sexpr(s[1])
        return "({})".format(" ".join(format_sexpr(e) for e in s))
    return repr(s)


def quines():
    q = Var()
    for s in run(5, q, eval_expr(q, (), q)):
        print(format_sexpr(s))


if __name__ == '__main__':
    quines()
