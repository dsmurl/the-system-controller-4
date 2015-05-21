import logging
import gevent
from peewee import SqliteDatabase
import config

DB = None


def background_service():
    """
    :return:
    """
    ctr = 0
    while 1:
        # do stuff here
        # logging.debug('{}'.format(ctr))
        ctr += 1
        gevent.sleep(1)


def get_db():
    """Get Application Database
    :return: DB
    """
    global DB
    if DB is None:
        DB = SqliteDatabase(config.db)

    return DB