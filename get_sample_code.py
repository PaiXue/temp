import json
import re
import javalang
from model import Traces, POIPackage, POIMultiClass, POIMethod


def get_method_by_id():
    pass


if __name__ == "__main__":
    schema_name = 'domainkg'

    with open('../data.json', 'r') as f:
        data = json.load(f)
        for line in data:
            trace_id = line['trace_id']
            code = line['code']
            method_record_id = line['method_record_id']
            print(trace_id)
            print(code)
            print(method_record_id)

            break
