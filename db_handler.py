from engine_factory import EngineFactory
from model import Traces
import json
import pandas as pd


def update_by_className_methodName_param(className, methodName, param, code, javadocComment, blockComment):
    trace = Traces(className, javadocComment, methodName, blockComment, param, code)
    try:
        trace.find_or_create(session, autocommit=False)
        # parameter_value.find_or_create(session=session, autocommit=False)
        # trace = session.query(Traces).filter_by(className=className, methodName=methodName, param=param).first()
        # trace.code = code
    except Exception:
        print("not find")
    return trace


def read_json_by_line(file_path):
    counter = 0
    step = 3000
    with open(file_path, encoding='UTF-8') as f:
        for line in f.readlines():
            dic = json.loads(line)
            code = dic['src: ']
            methodName = dic['methodName: ']
            className = dic['className: ']
            param = dic['param: ']
            javadocComment = dic['javadocComment: ']
            blockComment = dic['blockComment: ']

            update_by_className_methodName_param(className, methodName, param, code, javadocComment, blockComment)
            counter += 1
            if counter > step:
                counter = 0
                session.commit()
        session.commit()


if __name__ == "__main__":
    schema_name = 'domainkg'
    engine = EngineFactory.create_engine_by_schema_name(schema_name)
    session = EngineFactory.create_session(engine=engine, autocommit=False)
    read_json_by_line('traces.json')

    # trace_list = session.query(Traces).filter_by()
    # for trace in trace_list:
    #     try:
    #         className = trace.className
    #         methodName = trace.methodName
    #         param = trace.param
    #         trace.code = 'code'
    #     except Exception:
    #         print("error")
