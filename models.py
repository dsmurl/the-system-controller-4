import datetime
import json
from peewee import *
from playhouse.shortcuts import model_to_dict
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

    def to_client(self):

        return model_to_dict(self)

    def key(self, property_or_method=None):
        args = [self.__class__.__name__, self.id]

        if property_or_method and hasattr(self, property_or_method):
            args.append(property_or_method)

        return '/'.join(map(lambda arg: str(arg), args))

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


class Sensor(BaseModel):
    created = DateTimeField(default=datetime.datetime.now)

    label = CharField(index=False)
    pin = CharField(index=False)

    def value(self):
        # TODO implement sensor value get
        return '256'

    def to_client(self):

        data = model_to_dict(self)
        data['key'] = self.key('value')

        return data


class Device(BaseModel):
    created = DateTimeField(default=datetime.datetime.now)

    label = CharField(index=False)
    pin = CharField(index=False)
    value = BooleanField(index=False)

    def to_client(self):

        data = model_to_dict(self)
        data['key'] = self.key('value')

        return data


class Rule(BaseModel):
    created = DateTimeField(default=datetime.datetime.now)

    label = CharField(index=False)
    enabled = BooleanField(index=True, default=True)

    conditions = TextField(default='[]')

    action = TextField(default='[]')

    def set_conditions(self, conditions):
        """Sample Format:
            [
                Generating in code sample
                [entity.key('property_or_method'), str(operator), entity.key('property_or_method')],
                Actual value generated
                [Sensor/1/value, 'Equal', 1]
            ]
        """

        self.conditions = json.dumps(conditions)

    def get_conditions(self):

        return json.loads(self.conditions)

    def set_action(self, action):
        """Sample Format:
            [
                Generating in code sample
                [entity.key('property_or_method'), entity.key('property_or_method')],
                Actual value generated
                [Device/1, 1]
            ]
        """

        self.action = json.dumps(action)

    def get_action(self):

        return json.loads(self.action)

    def to_client(self):

        data = model_to_dict(self)
        data['conditions'] = self.get_conditions()
        data['action'] = self.get_action()

        return data


"""
Anything under this line are managers for the models
"""


def create_tables():
    """Creates all tables for models

    :return:
    """
    db = utils.get_db()
    db.connect()
    db.create_tables(utils.get_members_by_parent(__name__, BaseModel).values(), True)
    db.close()