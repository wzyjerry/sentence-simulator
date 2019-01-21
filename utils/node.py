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
        self.children = []
        self.weights = None

    def generate(self, entity_map, result={}):
        result = {
            'index': self.index,
            'type': self.data['type']
        }
        if 'name' in self.data:
            result['name'] = self.data['name']
        if self.data['type'] in ('root', 'intent'):
            i = weighted_sample(self.weights)
            if self.data['type'] == 'intent':
                result['intent'] = self.data['intent']
            ret = self.children[i].generate(entity_map)
            if ret is not None:
                result['children'] = [ret]
            return result
        else:
            if random.random() >= self.data['dropout']:
                if self.data['type'] == 'pickone':
                    i = weighted_sample(self.weights)
                    ret = self.children[i].generate(entity_map)
                    if ret is not None:
                        result['children'] = [ret]
                elif self.data['type'] == 'content':
                    text = None
                    if self.data['isSlot']:
                        text = entity_map[self.data['entity']]['entries'][random.choice(len(entity_map[self.data['entity']]['entries']))]
                        if self.data['slot'] == '':
                            result['entity'] = entity_map[self.data['entity']]['name']
                        else:
                            result['entity'] = self.data['slot']
                    else:
                        text = random.choice(self.data['content'])
                    if random.random() < self.data['cut']:
                        n_text = []
                        for ch in text:
                            if random.random() > self.data['word_cut']:
                                n_text.append(ch)
                        text = ''.join(n_text)
                    result['text'] = text
                else:
                    # order & exchangeable
                    children = []
                    for child in self.children:
                        ret = child.generate(entity_map)
                        if ret is not None:
                            children.append(ret)
                    if self.data['type'] == 'exchangeable':
                        index = range(len(children))
                        random.shuffle(list(index))
                        children = [children[i] for i in index]
                    if len(children):
                        result['children'] = children
            else:
                return None
        return result
