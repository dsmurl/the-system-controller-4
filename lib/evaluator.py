import logging

import operator
from lib import utils
from models.BaseModel import BaseModel


class Evaluator(object):

    def __init__(self, rule):
        self.rule = rule
        self.operators = utils.get_members_by_parent(operator, operator.Operator)

    def evaluate(self):
        """Runs through each rule conditions and execute rule action if conditions met
        :return:
        """

        for condition in self.rule.get_conditions():
            if not self._evaluate(condition):
                logging.debug('Not Executing action.')
                return False  # Found a condition that was false so bail

        return True

    def _evaluate(self, condition):
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
