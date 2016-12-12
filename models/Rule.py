from models.BaseModel import BaseModel
import logging
import datetime
import json
import gevent
from peewee import *
from playhouse.shortcuts import model_to_dict
from lib import utils, gpio, operator


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
            target, value = action

            device = self.get_by_key(target)

            if int(value):
                device.switch_on()
            else:
                device.switch_off()

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

        val1 = self.get_by_key(first + "/value")
        val2 = self.get_by_key(second)
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
