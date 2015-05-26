import logging
from lib.basehandler import RpcHandler
from lib.jsonrpc import ServerException


class ApiHandler(RpcHandler):

    def list_sensors(self):

        return [
            {
                'id': 1,
                'label': 'Moisture Sensor 1',
            },
            {
                'id': 2,
                'label': 'Moisture Sensor 2',
            },
            {
                'id': 3,
                'label': 'Moisture Sensor 3',
            },
            {
                'id': 4,
                'label': 'Thermistor 1',
            },
            {
                'id': 5,
                'label': 'Thermistor 2',
            },
            {
                'id': 6,
                'label': 'CO2 Sensor',
            },
            {
                'id': 7,
                'label': 'Water Level',
            }
        ]

    def list_devices(self):

        return [
            {
                'id': 1,
                'label': 'Maintanence Light',
            },
            {
                'id': 2,
                'label': 'Water Solenoid 1',
            },
            {
                'id': 3,
                'label': 'Water Solenoid 2',
            },
            {
                'id': 4,
                'label': 'Water Solenoid 3',
            },
            {
                'id': 5,
                'label': 'Fan 1',
            },
            {
                'id': 6,
                'label': 'Fan 2',
            }
        ]

    def list_rules(self):

        return [
            {
                'id': 1,
                'label': 'Turn on the maintenance light at night.',
            },
            {
                'id': 2,
                'label': 'Turn on water when moisture is low.',
            },
            {
                'id': 3,
                'label': 'Turn on fan when heat is high.',
            },
            {
                'id': 4,
                'label': 'Turn on the CO2 tank when CO2 is low.',
            }
        ]