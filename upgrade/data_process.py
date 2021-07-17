import json
import time


class FileOperate:
    def __init__(self):
        pass

    def read_json(self, file_name):
        with open(file_name, 'r') as rf:
            data = json.load(rf)
        return data

    def write_json(self, file_name, data):
        with open(file_name, 'w') as wf:
            json.dump(data, wf, indent=4)
        print('write file ok')

