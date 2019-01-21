import os
import codecs
from collections import Iterable

from numpy import array, float32

from utils.exception import raise_error
from utils.node import Node


def _check_set_float(node, data, key, default, min_val=None, max_val=None):
    if key in data:
        try:
            node.data[key] = float(data[key])
            if min_val is not None and node.data[key] < min_val:
                raise_error('Key %s must greater than %f.' % (key, min_val))
            if max_val is not None and node.data[key] > max_val:
                raise_error('Key %s must less than %f.' % (key, max_val))
        except ValueError as e:
            raise_error(e)
    else:
        node.data[key] = default


def _set_if_exist(node, data, key):
    if key in data:
        node.data[key] = data[key]


def hierarchy(data, parent=None, index=0):
    node = Node(parent)
    node.index = index
    index += 1
    stat = {
        # 【实体集合】
        'entity': set(),
        # 下一个可用的编号
        'index': index,
        # 统计信息
        'n_root': 0,
        'n_intent': 0,
        'n_pickone': 0,
        'n_order': 0,
        'n_exchangeable': 0,
        'n_content': 0,
        'n_tag': 0
    }
    # 检查每个节点类型，对于每种类型的节点，补全初始值，删除无效字段
    if 'type' not in data:
        raise_error(
            'Key "type" not found nearby "...%s...", a node must contains key "type".' % str(data)[:64])
    node.data['type'] = data['type']
    if node.data['type'] == 'root':
        pass
    elif node.data['type'] == 'holder':
        return (False, )
    elif node.data['type'] == 'intent':
        if 'intent' not in data:
            raise_error(
                'Key "intent" not found nearby "...%s...", intent node must contains key "intent".' % str(data)[:64])
        node.data['intent'] = data['intent']
        _check_set_float(node, data, 'dropout', 0.0, 0.0, 1.0)
        _check_set_float(node, data, 'weight', 1.0)
    elif node.data['type'] in ('pickone', 'order', 'exchangeable'):
        _set_if_exist(node, data, 'name')
        _check_set_float(node, data, 'dropout', 0.0, 0.0, 1.0)
        if parent != None and parent.data['type'] in ('pickone', 'intent'):
            _check_set_float(node, data, 'weight', 1.0)
    elif node.data['type'] == 'content':
        if 'isSlot' not in data:
            node.data['isSlot'] = False
            if 'isEntity' not in data:
                node.data['isSlot'] = False
            else:
                node.data['isSlot'] = bool(data['isEntity'])
        else:
            node.data['isSlot'] = bool(data['isSlot'])
        if node.data['isSlot']:
            if 'entity' not in data:
                raise_error(
                    'Key "entity" not found nearby "...%s...", slot content node must contains key "entity".' % str(data)[:64])
            node.data['entity'] = data['entity']
            stat['entity'].add(node.data['entity'])
            if 'slot' not in data:
                node.data['slot'] = ''
            else:
                node.data['slot'] = data['slot']
        else:
            if 'content' not in data or not isinstance(data['content'], Iterable):
                return (False, )
            node.data['content'] = []
            stat['n_tag'] += len(data['content'])
            for item in data['content']:
                node.data['content'].append(item)
        _set_if_exist(node, data, 'name')
        if parent != None and parent.data['type'] in ('pickone', 'intent'):
            _check_set_float(node, data, 'weight', 1.0)
        _check_set_float(node, data, 'dropout', 0.0, 0.0, 1.0)
        _check_set_float(node, data, 'cut', 0.0, 0.0, 1.0)
        if node.data['cut'] > 0.0:
            _check_set_float(node, data, 'word_cut', 0.0, 0.0, 1.0)
    else:
        raise_error(
            'Unknoe node type "%s" nearby "...%s...".' % (node.data['type'], str(data)[:64]))
    stat['n_' + node.data['type']] += 1
    # 叶节点返回
    if node.data['type'] == 'content':
        return True, node, stat
    # 添加子节点
    node.children = []
    if 'children' in data and isinstance(data['children'], Iterable):
        for child in data['children']:
            result = hierarchy(child, node, stat['index'])
            if result[0]:
                node.children.append(result[1])
                r_st = result[2]
                stat['entity'].update(r_st['entity'])
                stat['index'] = r_st['index']
                stat['n_intent'] += r_st['n_intent']
                stat['n_pickone'] += r_st['n_pickone']
                stat['n_order'] += r_st['n_order']
                stat['n_exchangeable'] += r_st['n_exchangeable']
                stat['n_content'] += r_st['n_content']
                stat['n_tag'] += r_st['n_tag']
    if len(node.children) == 0:
        return (False,)
    if node.data['type'] in ('root', 'pickone', 'intent'):
        node.weights = []
        for child in node.children:
            node.weights.append(child.data['weight'])
        node.weights = array(node.weights, dtype=float32)
    return True, node, stat


def str_stat(stat, entity_map):
    result = []
    result.append('Compile completed. Total nodes: %d' % stat['index'])
    result.append(
        'This syntax tree totally contains %d kind(s) of intent.' % stat['n_intent'])
    result.append('=' * 80)
    result.append('Node statistics:')
    result.append('Node pickone: %d' % stat['n_pickone'])
    result.append('Node order: %d' % stat['n_order'])
    result.append('Node exchangeable: %d' % stat['n_exchangeable'])
    result.append('Node content: %d' % stat['n_content'])
    result.append('-' * 20)
    result.append('Total tags: %d' % stat['n_tag'])
    result.append('=' * 80)
    result.append('Entity set:')
    for item in list(stat['entity']):
        result.append('%s --> %s' % (item, entity_map[item]['name']))
    result.append('=' * 80)
    result.append('Over.')
    return '\n'.join(result)


def link_entity(stat, entity):
    all_entity = {}
    for item in entity:
        all_entity[item['id']] = {
            'name': item['name'],
            'entries': item['entries']
        }
    entity_map = {}
    for item in list(stat['entity']):
        if item not in all_entity:
            raise_error('Entity "%s" not exists.' % item)
        entity_map[item] = all_entity[item]
    return entity_map


# def test():
#     import json
#     with codecs.open('data/syntaxTree.json', 'r', 'utf-8') as fin:
#         data = json.load(fin)
#         result = hierarchy(data)
#         if result[0]:
#             print(str_stat(result[2]))
#             check_file_set(result[2])


# if __name__ == '__main__':
#     test()
