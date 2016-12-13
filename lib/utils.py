import calendar
import inspect
import logging
import datetime
import gevent
from peewee import SqliteDatabase
import sys
import pkgutil
import config

DB = None
CLIENTS = []


def background_service():
    """
    :return:
    """
    while 1:

        gevent.sleep(1)


def get_db():
    """Get Application Database
    :return: DB
    """
    global DB
    if DB is None:
        DB = SqliteDatabase(config.db)

    return DB


def default_json_decode(obj):

    if isinstance(obj, datetime.datetime):
        if obj.utcoffset() is not None:
            obj = obj - obj.utcoffset()
    millis = int(
        calendar.timegm(obj.timetuple()) * 1000 +
        obj.microsecond / 1000
    )

    return millis


def get_members_by_parent_from_package(package, parent):
    """ Get all classes that extends 'parent' from a package

    :return:
    """

    children = {}
    prefix = package.__name__ + "."

    for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
        new_members = get_members_by_parent_from_module(modname, parent)
        children.update(new_members)

    return children


def get_members_by_parent_from_module(module, parent):
    """ Get all classes that extends 'parent' from a module

    :return:
    """
    return dict(member
                for member in inspect.getmembers(sys.modules[module if type(module) is str else module.__name__],
                                                 lambda c: inspect.isclass(c) and c.__base__ is parent))
