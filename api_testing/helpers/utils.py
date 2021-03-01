import json


def read_json(path):
    with open(path, mode='r', encoding='utf-8') as json_file:
        return json.load(json_file)


def list_transform_dict(content):
    return json.loads(content)
