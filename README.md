# microkanren

[![Build Status](https://travis-ci.com/ethframe/microkanren.svg?branch=master)](https://travis-ci.com/ethframe/microkanren)
[![codecov](https://codecov.io/gh/ethframe/microkanren/branch/master/graph/badge.svg)](https://codecov.io/gh/ethframe/microkanren)

Yet another microkanren implementation in Python. Still work in progress.

Features:
* Lists and namedtuples unification
* Disequality constraints
* Type constraints
* Reasonably fast non-relational arithmetic

### Example: bruteforce factorization

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

### Goal helpers

#### `mk.dsl`

* `@delay(goal_constructor)` - decorator for recursive goal constructors
* `fresh(goal_constructor)` - constructs goal that calls `goal_constructor` with fresh variable
* `fresh(n, goal_constructor)` - constructs goal that calls `goal_constructor` with `n` fresh variables

### Running goals

#### `mk.run`

* `run(n, query, goal)` - run `goal`, apply resulting substitution to `query`, take `n` first results
