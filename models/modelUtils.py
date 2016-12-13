import logging
import datetime
import json
import gevent
from peewee import *
from playhouse.shortcuts import model_to_dict
from models.BaseModel import BaseModel
from lib import utils, gpio, operator
import logging


"""
Anything under this line are managers for the models
"""


def create_tables():
    """Creates all tables for models

    :return:
    """
    db = utils.get_db()
    db.connect()
    import models

    db.create_tables(utils.get_members_by_parent_from_package(models, BaseModel).values(), True)
    db.close()
