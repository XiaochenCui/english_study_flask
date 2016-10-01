from vocabulary.models import Word


def serialize_instance(obj):
    """

    Args:
        obj:

    Returns:
        dict
    """
    d = {'__classname__': type(obj).__name__,}
    if isinstance(d, list):
        for i in d:
            d[id(i)] = serialize_instance(i)
    for key, value in vars(obj).items():
        if isinstance(value, str):
            d[key] = value
    return d


def serialize_list(l):
    d = {'__classname__': type(l).__name__,}
    for i in l:
        if isinstance(i, list):
            d[id(i)] = serialize_list(i)
        else:
            d[id(i)] = serialize_instance(i)
    return d


classes = {
    'Word': Word,
}


def unserialize_instance(d: dict):
    clsname = d.pop('__classname__', default=None)
    if (clsname):
        cls = classes[clsname]
        obj = cls.__new__(cls)
        for key, value in d.items():
            setattr(obj, key, value)
        return obj
    else:
        return d


if __name__ == '__main__':
    w = Word()
    w.word = 'haha'
    print(serialize_instance(w))
    a = Word()
    a.word = 'x'
    a.description = 'i dot know'
    s = serialize_list([w, a])
    print(s)
