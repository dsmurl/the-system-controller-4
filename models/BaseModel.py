import logging
import datetime
import json
import gevent
from peewee import *
from playhouse.shortcuts import model_to_dict
from lib import utils, gpio, operator
import logging


class BaseModel(Model):

    class Meta:
        database = utils.get_db()

    # Returns the Entity with the given id
    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.get(cls.id == id)
        except cls.DoesNotExist:
            return None

    # Converts this entity to a dictionary to be passed around
    def to_client(self):

        return model_to_dict(self)

    # Creates a key string that includes this entities name,
    # id, and a possible property_or_method.  All separated by /.
    def key(self, property_or_method=None):
        args = [self.__class__.__name__, self.id]

        if property_or_method and hasattr(self, property_or_method):
            args.append(property_or_method)

        return '/'.join(map(lambda arg: str(arg), args))

    # Retrieves an entity by it's key like "Sensor/1" or
    # gets a value of a key of this entity by something like
    # "Sensor/1/value"
    @classmethod
    def get_by_key(cls, key, default=None):
        if str(key).count('/') > 0:
            keys = key.split('/')
            model = keys.pop(0)
            primary_id = keys.pop(0)
            method = None
            if keys:
                method = keys.pop(0)

            entity = utils.get_members_by_parent(__name__, BaseModel)[model].get_by_id(int(primary_id))

            if not method:
                return entity
            elif hasattr(entity, method):
                val = getattr(entity, method)
                return val() if callable(val) else val

            return default

        return key

    # Retrieves an entity by a key like "Sensor/1" or "Sensor/1/value"
    @classmethod
    def get_entity_by_key(cls, key, default=None):
        if str(key).count('/') > 0:
            keys = key.split('/')
            model = keys.pop(0)
            primary_id = keys.pop(0)

            entity = utils.get_members_by_parent(__name__, BaseModel)[model].get_by_id(int(primary_id))

            return entity

        return None



