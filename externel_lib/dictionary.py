def get_the_value(d: dict):
    """
    对于长度为1的dict，返回那个唯一的val

    Args:
        d:
    """
    val = list(d.values())[0]
    return val


if __name__ == '__main__':
    a = {'first': 1}
    b = {'second':2}
    c = {'third': 3}
    d = {'four': 4}
    c = [d, a, c, b, a, c, b]
    print(c)
    print(get_the_value(a))
    print(get_the_value(b))
    c.sort(key=get_the_value)
    print(c)
    x = filter(lambda x:get_the_value(x)<2, c)
    print(list(x))
    print(c)