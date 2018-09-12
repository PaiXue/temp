from sqlalchemy import Column, Integer, String, Text, MetaData, ForeignKey, DateTime, Index, Boolean, func, Table, \
    SmallInteger, Float, or_
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import traceback

from engine_factory import EngineFactory

Base = declarative_base()


class Traces(Base):
    __tablename__ = 'traces'
    id = Column(Integer, primary_key=True, autoincrement=True)
    className = Column(String(255))
    javadocComment = Column(Text())
    methodName = Column(String(255))
    blockComment = Column(Text())
    param = Column(String(255))
    code = Column(LONGTEXT())

    def __init__(self, className, javadocComment, methodName, blockComment, param, code):
        self.className = className
        self.javadocComment = javadocComment
        self.methodName = methodName
        self.blockComment = blockComment
        self.param = param
        self.code = code

    def get_remote_object(self, session):
        if self.id:
            return self
        else:
            try:
                return session.query(Traces).filter_by(className=self.className,
                                                       javadocComment=self.javadocComment,
                                                       methodName=self.methodName,
                                                       blockComment=self.blockComment,
                                                       param=self.param,
                                                       code=self.code).first()
            except Exception:
                traceback.print_exc()
            return None

    def find_or_create(self, session, autocommit=True):
        remote_instance = self.get_remote_object(session)
        if not remote_instance:
            session.add(self)
            if autocommit:
                session.commit()
            return self
        else:
            return remote_instance


class CodeSample(Base):
    __tablename__ = 'code_sample'
    id = Column(Integer, primary_key=True, autoincrement=True)
    method_id = Column(Integer)
    description = Column(Text())
    type = Column(Integer)
    raw_code = Column(LONGTEXT)

    def __init__(self, method_id, description, type, raw_code):
        self.method_id = method_id
        self.description = description
        self.type = type
        self.raw_code = raw_code

    def get_remote_object(self, session):
        if self.id:
            return self
        else:
            try:
                return session.query(CodeSample).filter_by(method_id=self.method_id,
                                                           description=self.description,
                                                           type=self.type,
                                                           raw_code=self.raw_code,
                                                           ).first()
            except Exception:
                traceback.print_exc()
            return None

    def find_or_create(self, session, autocommit=True):
        remote_instance = self.get_remote_object(session)
        if not remote_instance:
            session.add(self)
            if autocommit:
                session.commit()
            return self
        else:
            return remote_instance


class POIPackage(Base):
    __tablename__ = 'poi_package'
    package_id = Column(Integer, primary_key=True, autoincrement=True)
    package_name = Column(String(255))
    package_url = Column(String(255))
    description = Column(String(1024))

    def __init__(self, package_name, package_url, description):
        self.package_name = package_name
        self.package_url = package_url
        self.description = description

    def get_remote_object(self, session):
        if self.package_id:
            return self
        else:
            try:
                return session.query(POIPackage).filter_by(package_name=self.package_name,
                                                       package_url=self.package_url,
                                                       description=self.description).first()
            except Exception:
                traceback.print_exc()
            return None

    def find_or_create(self, session, autocommit=True):
        remote_instance = self.get_remote_object(session)
        if not remote_instance:
            session.add(self)
            if autocommit:
                session.commit()
            return self
        else:
            return remote_instance


class POIMultiClass(Base):
    __tablename__ = 'poi_multi_class'
    id = Column(Integer, primary_key=True, autoincrement=True)
    package_name = Column(String(255))
    name = Column(String(255))
    url = Column(String(255))
    description = Column(String(1024))
    type = Column(Integer)

    def __init__(self, package_name, name, url, description, type):
        self.package_name = package_name
        self.name = name
        self.url = url
        self.description = description
        self.type = type

    def get_remote_object(self, session):
        if self.id:
            return self
        else:
            try:
                return session.query(POIMultiClass).filter_by(package_name=self.package_name,
                                                       name=self.name,
                                                       url=self.url,
                                                       type=self.type,
                                                       description=self.description).first()
            except Exception:
                traceback.print_exc()
            return None

    def find_or_create(self, session, autocommit=True):
        remote_instance = self.get_remote_object(session)
        if not remote_instance:
            session.add(self)
            if autocommit:
                session.commit()
            return self
        else:
            return remote_instance


class POIMethod(Base):
    __tablename__ = 'poi_method'
    method_id = Column(Integer, primary_key=True, autoincrement=True)
    package_name = Column(String(255))
    class_name = Column(String(255))
    return_type = Column(String(255))
    method_name = Column(String(512))
    description = Column(String(1024))
    type = Column(Integer)

    def __init__(self, package_name, class_name, return_type, method_name, description, type):
        self.package_name = package_name
        self.class_name = class_name
        self.return_type = return_type
        self.method_name = method_name
        self.description = description
        self.type = type

    def get_remote_object(self, session):
        if self.method_id:
            return self
        else:
            try:
                return session.query(POIMethod).filter_by(package_name=self.package_name,
                                                       class_name=self.class_name,
                                                       return_type=self.return_type,
                                                       method_name=self.method_name,
                                                       description=self.description,
                                                       type=self.type).first()
            except Exception:
                traceback.print_exc()
                session.rollback()
            return None

    def find_or_create(self, session, autocommit=True):
        remote_instance = self.get_remote_object(session)
        if not remote_instance:
            session.add(self)
            if autocommit:
                session.commit()
            return self
        else:
            return remote_instance


if __name__ == "__main__":
    engine = EngineFactory.create_engine_by_schema_name('domainkg')
    metadata = MetaData(bind=engine)

    # create the table
    Base.metadata.create_all(bind=engine)
