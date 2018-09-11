# import MySQLdb
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

metadata = MetaData()


class EngineFactory:
    @staticmethod
    def create_engine_to_center(echo=True):
        engine = create_engine("mysql+pymysql://root:root@10.141.221.87/domainkg?charset=utf8", encoding='utf-8',
                               echo=echo)
        return engine


    @staticmethod
    def create_engine_by_schema_name(schema_name, echo=True):
        if schema_name == 'stackoverflow':
            engine = create_engine("mysql+pymysql://root:root@10.131.252.160/stackoverflow?charset=utf8",
                                   encoding='utf-8',
                                   echo=echo)
            return engine
        elif schema_name == 'knowledgeGraph':
            engine = create_engine("mysql+pymysql://root:root@10.141.221.75/knowledgeGraph?charset=utf8",
                                   encoding='utf-8',
                                   echo=echo)
            return engine
        elif schema_name == 'codehub':
            engine = create_engine("mysql+pymysql://root:root@10.141.221.73/codehub?charset=utf8", encoding='utf-8',
                                   echo=echo)
            return engine
        elif schema_name == 'domainkg':
            engine = create_engine("mysql+pymysql://root:root@10.141.221.87/domainkg?charset=utf8", encoding='utf-8',
                                   echo=echo)
            return engine
        else:
            return None

    @staticmethod
    def create_session(engine=None, autocommit=False,echo=True):
        if engine is None:
            engine = EngineFactory.create_engine_to_center(echo=echo)

        Session = sessionmaker(bind=engine, autocommit=autocommit)
        session = Session()
        return session

