from .run import _reifiers
from .unify import _converters, _occurs_checkers, _unifiers


def register(key, *, convert=None, unify=None, occurs=None, reify=None):
    if convert:
        _converters.add(key, convert)
    if unify:
        _unifiers.add(key, unify)
    if occurs:
        _occurs_checkers.add(key, occurs)
    if reify:
        _reifiers.add(key, reify)


def register_exact(key, *, convert=None, unify=None, occurs=None, reify=None):
    if convert:
        _converters.add_exact(key, convert)
    if unify:
        _unifiers.add_exact(key, unify)
    if occurs:
        _occurs_checkers.add_exact(key, occurs)
    if reify:
        _reifiers.add_exact(key, reify)
