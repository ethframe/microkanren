def is_pair(p):
    return isinstance(p, tuple) and len(p) == 2


def list_to_pair(list_, recursive=False):
    pair = ()
    for i in reversed(list_):
        if recursive and isinstance(i, list):
            i = list_to_pair(i, True)
        pair = (i, pair)
    return pair


def pair_to_list(pair, recursive=False):
    list_ = []
    while is_pair(pair):
        i, pair = pair
        if recursive and is_pair(i):
            i = pair_to_list(i, True)
        list_.append(i)
    if pair != ():
        raise ValueError()
    return list_
