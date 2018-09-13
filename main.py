import codecs
import json

from numpy import random

from utils.tag import tag_iobes
from utils.hierarchy import check_file_set, hierarchy, str_stat
from utils.output import Output


def main():
    with codecs.open('data/syntaxTree.json', 'r', 'utf-8') as fin:
        data = json.load(fin)
        result = hierarchy(data)
        if result[0]:
            file_map = check_file_set(result[2])
            root = result[1]
            print(str_stat(result[2]))
            output = Output(root, file_map)
            output.addOutput(Output.DEBUG_LEVEL, 'data/out/debug.txt', tag_iobes)
            output.addOutput(Output.CHAR_LEVEL, 'data/out/char.txt', tag_iobes)
            output.addOutput(Output.WORD_LEVEL, 'data/out/word.txt', tag_iobes)
            output.addOutput(Output.SENTENCE_LEVEL, 'data/out/sentence.txt', tag_iobes)
            output.generate(100)


if __name__ == '__main__':
    random.seed(0)
    main()
