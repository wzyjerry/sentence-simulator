from numpy import random


def weighted_sample(weights):
    weights /= weights.sum()
    rand_num, accu = random.random(), 0.0
    for i in range(len(weights)):
        accu += weights[i]
        if accu >= rand_num:
            return i


class Node(object):
    def __init__(self, parent):
        self.index = None
        self.data = {}
        self.parent = parent
        self.children = None
        self.weights = None

    def generate(self, file_map):
        result = []
        result.append(('B-%d' % self.index, None, None))
        if self.data['type'] in ('root', 'intent', 'pick_one'):
            i = weighted_sample(self.weights)
            if self.data['type'] == 'intent':
                result[-1] = ('B-%d' % self.index, None, self.data['intent'])
            result.extend(self.children[i].generate(file_map))
            result.append(('I-%d' % self.index, None, None))
        else:
            if random.random() >= self.data['dropout']:
                if self.data['type'] == 'content':
                    text = None
                    if self.data['from_file']:
                        text = random.choice(file_map[self.data['filename']])
                    else:
                        text = random.choice(self.data['content'])
                    if random.random() < self.data['cut']:
                        n_text = []
                        for ch in text:
                            if random.random() > self.data['word_cut']:
                                n_text.append(ch)
                        text = ''.join(n_text)
                    result.append(('I-%d' % self.index, text, self.data.get('entity')))
                else:
                    # order & exchangeable
                    returns = []
                    for child in self.children:
                        ret = child.generate(file_map)
                        ret.append(('I-%d' % self.index, None, None))
                        returns.append(ret)
                    if self.data['type'] == 'exchangeable':
                        index = range(len(returns))
                        random.shuffle(list(index))
                        returns = [returns[i] for i in index]
                    for item in returns:
                        result.extend(item)
        result[-1] = ('E-%d' % self.index, result[-1][1], result[-1][2])
        return result
