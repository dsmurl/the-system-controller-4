import datetime
import inspect
from peewee import *
import sys
from lib import utils


class BaseModel(Model):

    class Meta:
        database = utils.get_db()

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.get(cls.id == id)
        except cls.DoesNotExist:
            return None


class Sensor(BaseModel):
    created = DateTimeField(default=datetime.datetime.now)
    controller_id = IntegerField(null=True)

    label = CharField(index=False)


"""
Anything under this line are managers for the models
"""


def base_models_predicate(c):
    """Filters all classes that extends BaseModel

    :param c:
    :return:
    """
    return inspect.isclass(c) and c.__base__ is BaseModel


def get_models():
    """Get all models that extends BaseModel

    :return:
    """
    return [model[1] for model in inspect.getmembers(sys.modules[__name__], base_models_predicate)]


def get_model_by_name(name):
    """Get a model by its name

    :return:
    """
    for model in get_models():
        if model.__name__ == name:
            return model


def create_tables():
    """Creates all tables for models

    :return:
    """
    db = utils.get_db()
    db.connect()
    db.create_tables(get_models(), True)
    db.close()