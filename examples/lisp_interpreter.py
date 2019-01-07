from collections import namedtuple

from mk.core import conj, disj, eq, eqt
from mk.disequality import neq
from mk.dsl import conde, conjp, delay, fresh
from mk.ext.lists import no_item
from mk.run import run
from mk.unify import Var


class Ident(str):
    def __repr__(self):
        return self

    def __eq__(self, other):
        return type(self) is type(other) and super().__eq__(other)


class Symbol(Ident):
    pass


class Builtin(Ident):
    pass


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


def is_internal(a):
    return isinstance(a, (Closure, Builtin))


quote, list_, lambda_ = map(Symbol, "quote list lambda".split())
car, cdr = map(Symbol, "car cdr".split())
car_fn, cdr_fn = map(Builtin, "car cdr".split())


def builtin(fn, out):
    return conde(
        (eq(fn, car), eq(out, car_fn)),
        (eq(fn, cdr), eq(out, cdr_fn)),
    )


def eval_builtin(fn, arg, out):
    return fresh(lambda t: conde(
        (eq(fn, car_fn), eq([out, t, ...], arg)),
        (eq(fn, cdr_fn), eq([t, out, ...], arg)),
    ))


@delay
def eval_expr(exp, env, out):
    return conde(
        (
            eq([quote, out], exp), no_item(out, is_internal),
            missing(quote, env),
        ),
        fresh(lambda lst: conjp(
            eq([list_, lst, ...], exp),
            missing(list_, env), eval_list(lst, env, out),
        )),
        fresh(5, lambda fn, arg, var, body, cenv: conj(
            eval_list(exp, env, [fn, arg]),
            conde(
                eval_builtin(fn, arg, out),
                (
                    eq(Closure(var, body, cenv), fn),
                    eval_expr(body, Env(var, arg, cenv), out),
                ),
            )
        )),
        fresh(2, lambda var, body: conjp(
            eq([lambda_, [var], body], exp), eq(Closure(var, body, env), out),
            eqt(var, Symbol), missing(lambda_, env),
        )),
        (eqt(exp, Symbol), lookup(exp, env, out)),
        (builtin(exp, out), missing(exp, env)),
    )


def format_sexpr(s):
    if isinstance(s, list):
        if len(s) == 2 and s[0] == Symbol("quote"):
            return "'" + format_sexpr(s[1])
        return "({})".format(" ".join(format_sexpr(e) for e in s))
    if s is Ellipsis:
        return "..."
    return repr(s)


def quines():
    q = Var()
    for s in run(5, q, eval_expr(q, (), q)):
        print(format_sexpr(s))


def generate_fn():
    q = Var()
    a = Symbol("a")
    env = Env(Symbol("cadr"), Closure(a, [car, [cdr, a]], ()), ())
    p = conj(
        no_item(q, lambda a: isinstance(a, int)),
        eval_expr([q, [quote, [1, 2, 3]]], env, [1, 2])
    )
    for s in run(5, q, p):
        print(format_sexpr(s))


if __name__ == '__main__':
    quines()
    generate_fn()
