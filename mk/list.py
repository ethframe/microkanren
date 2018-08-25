from .core import is_pair


def list_to_pair(list_):
    pair = ()
    for i in reversed(list_):
        pair = (i, pair)
    return pair


def pair_to_list(pair):
    list_ = []
    while is_pair(pair):
        i, pair = pair
        list_.append(i)
    if pair != ():
        raise ValueError()
    return list_
