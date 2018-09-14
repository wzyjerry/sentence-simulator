def generate(node):
  result = node.data
  result['index'] = node.index
  if len(node.children):
    result['children'] = []
    for child in node.children:
      result['children'].append(generate(child))
  return result
