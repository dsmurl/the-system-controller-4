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
    # getting a value of a key of this entity by something like
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


class Sensor(BaseModel):
    created = DateTimeField(default=datetime.datetime.now)

    label = CharField(index=False)
    pin = CharField(index=False)

    def value(self):

        logging.debug("Running read_sensor " + self.pin + "...")
        reading = gpio.read(self.pin)
        logging.debug("Done with read_sensor.  " + self.pin + " =>  " + str(reading))

        return reading

    def to_client(self):

        data = model_to_dict(self)
        data['key'] = self.key('value')

        return data


class Device(BaseModel):
    created = DateTimeField(default=datetime.datetime.now)

    label = CharField(index=False)
    pin = CharField(index=False)
    value = BooleanField(index=False)

    def switch_on(self):
        # todo implement switch
        return True

    def switch_off(self):
        # todo implement switch
        return False

    def to_client(self):

        data = model_to_dict(self)
        data['key'] = self.key('value')

        return data


class Rule(BaseModel):
    created = DateTimeField(default=datetime.datetime.now)

    label = CharField(index=False)
    enabled = BooleanField(index=True, default=True)

    conditions = TextField(default='[]')
    actions = TextField(default='[]')
    operators = utils.get_members_by_parent(operator, operator.Operator)

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

    def set_actions(self, actions):
        """Sample Format:
            [
                Generating in code sample
                [entity.key('property_or_method'), entity.key('property_or_method')],
                Actual value generated
                [Device/1, 1]
            ]
        """

        self.actions = json.dumps(actions)

    def get_actions(self):

        return json.loads(self.actions)

    def run(self):
        # Evaluate this rules conditions
        evaluation = self.evaluate_all_conditions()

        # Run the action if needed
        if evaluation:
                self.execute_action()

        return evaluation

    def execute_action(self):
        """ Executes the action associated with the rule
        :return:
        """

        logging.debug('Executing action.')

        for action in self.get_actions():
            # action = models.BaseModel.get_by_key(action)

            logging.debug('Executed: {} Result: {}'.format(action, 0))
            return

    def evaluate_all_conditions(self):
        """Runs through each rule conditions and execute rule action if conditions met
        :return:
        """

        for condition in self.get_conditions():
            if not self._evaluate_condition(condition):
                logging.debug('Not Executing action.')
                return False  # Found a condition that was false so bail

        return True

    def _evaluate_condition(self, condition):
        """Runs through a single condition and returns True or False
        :param condition:
        :return:
        """

        first, op, second = condition

        val1 = BaseModel.get_by_key(first)
        val2 = BaseModel.get_by_key(second)
        op_val = self.operators[op]()
        result = op_val.evaluate(val1, val2)

        logging.debug('Evaluate: {} {} {}'.format(val1, op_val, val2))

        return result

    def to_client(self):

        data = model_to_dict(self)
        data['conditions'] = self.get_conditions()
        data['actions'] = self.get_actions()

        return data

    @classmethod
    def background_run_rules(cls):

        while True:
            rules = cls.select()

            for rule in rules:
                rule.run()

            gevent.sleep(1)  # todo we can make the sleep system settings


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