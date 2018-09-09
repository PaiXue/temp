import pandas as pd
import json


def read_json_file(file_path):
    with open(file_path, encoding='UTF-8') as f:
        for line in f.readlines():
            dic = json.loads(line)
            print(dic)



if __name__ == "__main__":
    code_trace_pd = read_json_file('code_trace.json')
