import logging
from lib.basehandler import RpcHandler
from lib.jsonrpc import ServerException
import models
import Adafruit_BBIO.GPIO as GPIO

class ApiHandler(RpcHandler):

    def list_sensor(self):

        sensors = models.Sensor.select().order_by(models.Sensor.label)

        return [sensor.to_client() for sensor in sensors]

    def get_sensor(self, sensor_id):

        sensor = models.Sensor.get_by_id(sensor_id)

        if not sensor:
            sensor = models.Sensor()

        return sensor.to_client()

    def save_sensor(self, data):
        id = data.get('id')
        if id:
            sensor = models.Sensor.get_by_id(id)
        else:
            sensor = models.Sensor()

        sensor.label = data.get('label')
        sensor.code = data.get('code')
        sensor.save()

        return sensor.to_client()

    def delete_sensor(self, sensor_id):

        sensor = models.Sensor.get_by_id(sensor_id)

        if sensor:
            sensor.delete_instance()
            return True
        return False
    
    def list_device(self):

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

    def list_rule(self):

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

    def toggle_led(self, on_off):

        logging.debug("Running toggle_led...")
        logging.debug(on_off)

        GPIO.setup("P9_11", GPIO.OUT)
        if on_off:
            GPIO.output("P9_11", GPIO.HIGH)
            logging.debug("Setting P9_11 to HIGH")
        else:
            GPIO.output("P9_11", GPIO.LOW)
            logging.debug("Setting P9_11 to LOW")
        # GPIO.cleanup()   # Doesn't need to cleanup here, but somewhere as closing or something

        logging.debug("Done with toggle_led")

        return on_off

