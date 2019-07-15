import json


def insert(filepath, item):
    with open(filepath, 'a', encoding='utf-8') as f:
        f.write(json.dumps(item, ensure_ascii=False, indent=2) + '\n')
