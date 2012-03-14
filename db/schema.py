# -*- coding: utf-8 -*-
import os
import sys
import datetime

from sqlalchemy import create_engine, Table, Column, MetaData, ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.sql import select, and_, or_, not_, exists
from sqlalchemy.types import Unicode, Integer, Boolean, String, Date, DateTime, Enum, UnicodeText
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import mapper, sessionmaker, relation, backref, class_mapper, aliased, relationship
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base, declared_attr

import common.config as config
from common.log import logger

log = logger("db")

class DBObject(object):
    """
    This is the DBObject class which all other model classes rely on.
    It allows us to instantiate an object with attributes simply by passing
    them into the constructor.

    """
    def __init__(self, **kw):
        #log.debug("__init__:")
        for item, value in kw.iteritems():
            #log.debug("\t  %s=%s" % (item, value))
            setattr(self, item, value)

    def __iter__(self):
        """Implement iterator support: allow converting our objects to a dict"""
        def convert_datetime(value):
            return value.strftime("%Y-%m-%d %H:%M:%S") if value else value

        def convert_date(value):
            return value.strftime("%Y-%m-%d") if value else value

        d = {}
        for c in class_mapper(self.__class__).mapped_table.columns:
            if isinstance(c.type, DateTime):
                value = convert_datetime(sqlalchemy.orm.attributes.get_attribute(self, c.name))
            elif isinstance(c.type, LargeBinary):
                value = '%s' % sqlalchemy.orm.attributes.get_attribute(self, c.name)
            elif isinstance(c.type, Date):
                value = convert_date(sqlalchemy.orm.attributes.get_attribute(self, c.name))
            else:
                value = sqlalchemy.orm.attributes.get_attribute(self, c.name)

            yield(c.name, value)

class SABase(DBObject):
    """
    Base class which provides automated table name
    and surrogate primary key column.

    """
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, default=datetime.datetime.now)
    lastmodified = Column(DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now)

metadata = MetaData()
SABase = declarative_base(cls=SABase, metadata=metadata)

class Child(SABase):
    """
    A child. All students are children but not the converse.
    """

    __tablename__ = 'child'

    name = Column(UnicodeText, nullable=False)
    dob = Column(DateTime, nullable=False)
    sex = Column(Enum('male', 'female', 'tg', name='sex'))
    deleted = Column(Boolean, default=None, nullable=True)

    def __init__(self, name, dob, sex):
        self.name = name
        self.dob = dob
        self.sex = sex
        
    def __repr__(self):
        return "<Child #%s(%s, %s)>" % (self.id, self.name, self.dob)


def init_model(dburi):
    """Create a connection to the DB"""
    
    engine = create_engine(dburi, echo=False, pool_recycle=3600, convert_unicode=True)
    sess = sessionmaker(bind=engine)()

    log.info("connecting to DB %s:%s@%s/%s" %
              (engine.url.drivername,engine.url.username, engine.url.host,engine.url.database))

    return SABase.metadata, sess, engine
