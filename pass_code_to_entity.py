from engine_factory import EngineFactory
from model import Traces
import json
import pandas as pd
from sqlalchemy import text
import re
import javalang
from model import Traces, POIPackage, POIMultiClass, POIMethod


def query_method(str, context, qute_counter):
    if str == 'allocateShapeId':
        print("hi")
    str += '​%'

    method_object_list = session.query(POIMethod).filter(POIMethod.method_name.like(str)).all()

    if len(method_object_list) == 0 or method_object_list is None:
        return None
    if len(method_object_list) == 1:
        for m in method_object_list:
            return m
    record_list = []
    if len(method_object_list) > 1:
        for i, m in enumerate(method_object_list):
            # class_name = m.method_name
            # class_name_split = set(class_name.split('.'))
            # if len(class_name_split & context) > 0:
            record_list.append(m)

        if len(record_list) == 1:
            return record_list[0]
        else:
            for i, m in enumerate(method_object_list):
                method_name = m.method_name
                method_name = method_name
                method_name_split = method_name.split(',')
                small_context = re.split(r'[.,()\s]', method_name)
                if qute_counter == len(method_name_split) - 1 and len(set(small_context) & context) > 0:
                    return m
            return None


def match_string_to_method(input_str):
    input_str += '('
    pass


if __name__ == "__main__":
    schema_name = 'domainkg'
    word_set = {'+', '-', '<', '>', '=', '*', '/', '//', '&', '%', '!', '~', 'public', 'static', 'void', 'abstract',
                'default', 'double', 'else', 'enum', 'extends', 'final', 'finally', 'float', 'for', 'goto', 'if',
                'implements', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'package', 'private',
                'protected', 'return', 'short', 'static', 'strictfp', 'super', 'switch', 'synchronized', 'this',
                'throw', 'throws', 'transient', 'try', 'volatile', 'strictfp', 'while', 'Integer', 'String', 'Float',
                'Double', 'File', 'Object', '@throws', 'args', '@param', 'boolean', 'Boolean', 'True', 'False', 'byte',
                'byte[]', '(', ')', '.', ':', ';', '"', '|', '||', 'true', 'false', ','}
    engine = EngineFactory.create_engine_by_schema_name(schema_name)
    session = EngineFactory.create_session(engine=engine, autocommit=False, echo=False)
    trace_list = session.query(Traces).all()
    json_data = list()
    json_conuter = 0
    for trace in trace_list:
        # trace = session.query(Traces).filter_by(id=id).first()
        code = trace.code
        word_context_set = set()
        code_list = re.split(r'[{;}]', code)
        related_method_list = []
        for line in code_list:
            line = line.strip()
            if line != '\n' and line != '':
                print(line)
                line += ' '
                tokens = javalang.tokenizer.tokenize(line)
                qute_counter = len(line.split(',')) - 1
                try:
                    tokenList = list(tokens)
                    for i, t in enumerate(tokenList):
                        if t.value not in word_set:
                            word_context_set.add(t.value)
                            if i < len(tokenList) - 1 and tokenList[i + 1].value == '(':
                                query_result = query_method(t.value, word_context_set, qute_counter)
                                if query_result is not None:
                                    related_method_list.append(query_result)
                except Exception:
                    print("error")
                    continue

        print(len(related_method_list))        # json_data.append({"trace_id": trace.id, "code": trace.code, "method_record_id": list(method_id_set)})
        # json_conuter += 1
        # if json_conuter > 100:
        #     break
        method_id_set = set()
        for r_m in related_method_list:
            method_id_set.add(r_m.method_id)
        print(method_id_set)
        json_data.append({"trace_id": trace.id, "code": trace.code, "method_record_id": list(method_id_set)})

    with open('data.json', 'w') as outfile:
        json.dump(json_data, outfile)
