from engine_factory import EngineFactory
from model import Traces
import json
import pandas as pd
from sqlalchemy import text
import re
import javalang
from model import Traces, POIPackage, POIMultiClass, POIMethod

if __name__ == "__main__":
    schema_name = 'domainkg'
    engine = EngineFactory.create_engine_by_schema_name(schema_name)
    session = EngineFactory.create_session(engine=engine, autocommit=False, echo=False)
    poi_method_list = session.query(POIMethod).all()
