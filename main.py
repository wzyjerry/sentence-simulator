import codecs
import json

from utils.hierarchy import hierarchy, check_file_set, str_stat


def main():
    with codecs.open('data/syntaxTree.json', 'r', 'utf-8') as fin:
        data = json.load(fin)
        result = hierarchy(data)
        if result[0]:
            file_map = check_file_set(result[2])
            root = result[1]
            print(str_stat(result[2]))
            print(root.generate(file_map))


if __name__ == '__main__':
    main()
