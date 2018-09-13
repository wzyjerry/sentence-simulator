import codecs


def output(result, level, tag, fout):
    '''
    调试级: '%node\t%text\n'
    字符级: '%char\t%eneity\n'
    词级: '%word\t%entity\n'
    句级: '%intent\t%sentence'
    '''
    intent = None
    sentence = []
    content = []
    for item in result:
        if level == Output.DEBUG_LEVEL:
            content.append('%s\t%s\n' % (item[0], item[1]))
        elif item[1] is not None:
            sentence.append(item[1])
            token = item[1]
            if level == Output.WORD_LEVEL:
                token = token.split()
            temp = []
            for text in zip(list(token), tag(len(token), item[2])):
                temp.append('%s\t%s\n' % text)
            if level == Output.CHAR_LEVEL and len(content):
                content.append(' \tO\n')
            content.extend(temp)
        elif item[2] is not None:
            intent = item[2]
    if level == Output.SENTENCE_LEVEL:
        fout.write('%s\t%s\n' % (intent, ' '.join(sentence)))
    else:
        for item in content:
            fout.write(item)
        fout.write('\n')


class Output(object):
    DEBUG_LEVEL = 1
    CHAR_LEVEL = 2
    WORD_LEVEL = 3
    SENTENCE_LEVEL = 4

    def __init__(self, root, file_map):
        self.__root = root
        self.__file_map = file_map
        self.__outputs = []

    def addOutput(self, level, filename, tag):
        self.__outputs.append((level, filename, tag))

    def generate(self, num=None):
        if num is None:
            result = self.__root.generate(self.__file_map)
            for item in self.__outputs:
                with codecs.open(item[1], 'a', 'utf-8') as fout:
                    output(result, item[0], item[2], fout)
        else:
            file_list = []
            for item in self.__outputs:
                file_list.append(codecs.open(item[1], 'w', 'utf-8'))
            for i in range(num):
                result = self.__root.generate(self.__file_map)
                for item in zip(self.__outputs, file_list):
                    output(result, item[0][0], item[0][2], item[1])
                    item[1].flush()
            for item in file_list:
                item.close()
