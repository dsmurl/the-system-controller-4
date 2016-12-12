from models.BaseModel import BaseModel
import logging
import datetime
import json
import gevent
from peewee import *
from playhouse.shortcuts import model_to_dict
from lib import utils, gpio, operator


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
        data['key'] = self.key()

        return data

    @classmethod
    def background_send_values(cls):

        while True:
            clients = utils.CLIENTS
            sensors = cls.select()

            if sensors.count() > 0 and len(clients) > 0:
                data = dict((sensor.id, sensor.value()) for sensor in sensors)

                for client in clients:
                    client.send(json.dumps({
                        'event': 'sensors',
                        'result': data
                    }))

            gevent.sleep(1)
