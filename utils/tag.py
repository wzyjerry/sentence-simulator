def tag_iob2(len, entity):
    if entity is None:
        return ['O'] * len
    tag = ['I-%s' % entity] * len
    if len > 0:
        tag[0] = 'B-%s' % entity
    return tag


def tag_iobs(len, entity):
    if len == 1 and entity is not None:
        return ['S-%s' % entity]
    return tag_iob2(len, entity)


def tag_iobes(len, entity):
    tag = tag_iobs(len, entity)
    if len > 1 and entity is not None:
        tag[-1] = 'E-%s' % entity
    return tag


def test():
    print(tag_iob2(10, None))
    print(tag_iob2(5, 'place'))
    print(tag_iob2(2, 'date'))
    print(tag_iob2(1, 'name'))
    print(tag_iob2(0, 'inst'))
    print('---')
    print(tag_iobs(10, None))
    print(tag_iobs(5, 'place'))
    print(tag_iobs(2, 'date'))
    print(tag_iobs(1, 'name'))
    print(tag_iobs(0, 'inst'))
    print('---')
    print(tag_iobes(10, None))
    print(tag_iobes(5, 'place'))
    print(tag_iobes(2, 'date'))
    print(tag_iobes(1, 'name'))
    print(tag_iobes(0, 'inst'))


if __name__ == '__main__':
    test()
