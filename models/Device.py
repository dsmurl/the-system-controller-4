from models.BaseModel import BaseModel
import logging
import datetime
import json
import gevent
from peewee import *
from playhouse.shortcuts import model_to_dict
from lib import utils, gpio, operator


class Device(BaseModel):
    created = DateTimeField(default=datetime.datetime.now)

    label = CharField(index=False)
    pin = CharField(index=False)
    value = BooleanField(index=False)

    def switch_on(self):
        gpio.output_high(self.pin)
        return True

    def switch_off(self):
        gpio.output_low(self.pin)
        return False

    def to_client(self):

        data = model_to_dict(self)
        data['key'] = self.key()

        return data
