# -*- coding: utf-8 -*-

import datetime
from sqlalchemy.orm.exc import NoResultFound

import db.schema as schema
from common.log import logger
from .exceptions import NoSuchChild

log = logger("api:child")

def create(s, name, dob, sex):
    """
    Create a new child. Returns id of the newly created child.
    """
    child = schema.Child(name, dob, sex)
    s.add(child)
    s.flush()
    log.debug("Created %s" % child)

    return child.id
    
def delete(s, id):
    """
    Delete a child, by id.
    """
    try:
        child = s.query(schema.Child).get(id)
        child.deleted = True
        s.merge(child)
        s.flush()
    except NoResultFound:
        raise NoSuchChild(id)

def really_delete(s, id):
    """
    Delete a child, by id.
    """
    try:
        child = s.query(schema.Child).get(id)
        s.delete(child)
        s.flush()
    except NoResultFound:
        raise NoSuchChild(id)

def get(s, id):
    """
    Get a child, by id.
    """
    try:
        return s.query(schema.Child).get(id)
    except NoResultFound:
        raise NoSuchChild(id)
