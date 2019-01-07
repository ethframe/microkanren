# microkanren

[![Build Status](https://img.shields.io/travis/com/ethframe/microkanren/master.svg?logo=travis)](https://travis-ci.com/ethframe/microkanren)
[![codecov](https://img.shields.io/codecov/c/github/ethframe/microkanren/master.svg?logo=codecov)](https://codecov.io/gh/ethframe/microkanren)

Yet another microkanren implementation in Python. Still work in progress.

Features:
* Lists and namedtuples unification
* Disequality constraints
* Type constraints
* Reasonably fast non-relational arithmetic

## Examples

### Bruteforce factorization

```python
from mk.arithmetic import add, lte, mul
from mk.core import disj, eq
from mk.dsl import conjp, delay, fresh
from mk.run import run
from mk.unify import Var


@delay
def numbers(a, b, out):
    return disj(
        eq(a, out),
        fresh(lambda n: conjp(
            add(a, 1, n),
            lte(n, b),
            numbers(n, b, out)
        ))
    )


a = Var()
b = Var()
goal = conjp(
    numbers(0, 256, a),
    mul(a, b, 65535)
)

print(list(run(0, (a, b), goal)))
# [(1, 65535), (3, 21845), (5, 13107), (15, 4369),
#  (17, 3855), (51, 1285), (85, 771),  (255, 257)]
```

### Lisp-like language interpreter (without auxiliary code)

Full source with quines generation: [examples/lisp_interpreter.py](https://github.com/ethframe/microkanren/blob/0623d11b026be2428289d351cdcb75b3cd01d617/examples/lisp_interpreter.py)

```python
from mk.core import eq, eqt
from mk.dsl import conde, conjp, delay, fresh
from mk.ext.lists import no_item


@delay
def eval_expr(exp, env, out):
    return conde(
        # Quoted value - 'a
        (eq([quote, out], exp), no_item(out, is_closure), missing(quote, env)),
        # List constructor - (list a b c)
        fresh(lambda lst: conjp(
            eq([list_, lst, ...], exp),
            missing(list_, env), eval_list(lst, env, out),
        )),
        # Function call - (fn a)
        fresh(4, lambda var, body, cenv, arg: conjp(
            eval_list(exp, env, [Closure(var, body, cenv), arg]),
            eval_expr(body, Env(var, arg, cenv), out),
        )),
        # Function definition - (lambda (x) body)
        fresh(2, lambda var, body: conjp(
            eq([lambda_, [var], body], exp), eq(Closure(var, body, env), out),
            eqt(var, Symbol), missing(lambda_, env),
        )),
        # Variable reference - a
        (eqt(exp, Symbol), lookup(exp, env, out)),
    )
```

## API summary

### Goal constructors

#### `mk.core`

* `eq(a, b)` - construct goal that succeeds when `a` can be unified with `b`
* `eqt(a, b)` - construct goal that succeeds when type of `a` can be unified with `b`
* `disj(goal_1, goal_2)` - construct composite goal that succeeds when `goal_1` or `goal_2` succeed
* `conj(goal_1, goal_2)` - construct composite goal that succeeds when both `goal_1` and `goal_2` succeed

#### `mk.disequality`

* `neq(a, b)` - negation of `eq(a, b)`
* `neqt(a, b)` - negation of `eqt(a, b)`

#### `mk.arithmetic`

* `add(a, b, c)` - construct goal that succeeds when `a + b == c`
* `sub(a, b, c)` - construct goal that succeeds when `a - b == c`
* `mul(a, b, c)` - construct goal that succeeds when `a * b == c`
* `div(a, b, c)` - construct goal that succeeds when `a // b == c`
* `gte(a, b)` - construct goal that succeeds when `a >= b`
* `lte(a, b)` - construct goal that succeeds when `a <= b`

#### `mk.dsl`

* `disjp(goal, ...)` - n-ary `disj`
* `conjp(goal, ...)` - n-ary `conj`
* `conde((goal, ...), (goal, ...), ...)` - shortcut for `disjp(conjp(goal, ...), conjp(goal, ...), ...)`

#### `mk.ext.lists`

* `no_item(a, predicate)` - construct goal that fails when `a` is list that contains item, possibly in nested list, for which `predicate` is true.

#### `mk.ext.tuples`

* `no_item(a, predicate)` - construct goal that fails when `a` is tuple that contains item, possibly in nested tuple, for which `predicate` is true.

### Goal helpers

#### `mk.dsl`

* `@delay(goal_constructor)` - decorator for recursive goal constructors
* `fresh(goal_constructor)` - constructs goal that calls `goal_constructor` with fresh variable
* `fresh(n, goal_constructor)` - constructs goal that calls `goal_constructor` with `n` fresh variables

### Running goals

#### `mk.run`

* `run(n, query, goal)` - run `goal`, apply resulting substitution to `query`, take `n` first results
