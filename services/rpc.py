import logging
from lib import utils, operator, evaluator
from lib.basehandler import RpcHandler
from lib.jsonrpc import ServerException
import models
import Adafruit_BBIO.GPIO as GPIO

class ApiHandler(RpcHandler):

    # Sensor Section
    def list_sensor(self):

        sensors = models.Sensor.select().order_by(models.Sensor.id)

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
        sensor.pin = data.get('pin')
        sensor.save()

        return sensor.to_client()

    def delete_sensor(self, sensor_id):

        sensor = models.Sensor.get_by_id(sensor_id)

        if sensor:
            sensor.delete_instance()
            return True
        return False

    # Device Section
    def list_device(self):

        devices = models.Device.select().order_by(models.Device.id)

        return [device.to_client() for device in devices]

    def get_device(self, device_id):

        device = models.Device.get_by_id(device_id)

        if not device:
            device = models.Device()

        return device.to_client()

    def save_device(self, data):
        id = data.get('id')
        if id:
            device = models.Device.get_by_id(id)
        else:
            device = models.Device()

        device.label = data.get('label')
        device.pin = data.get('pin')
        device.value = False    # Always starts as False
        device.save()

        return device.to_client()

    def delete_device(self, device_id):

        device = models.Device.get_by_id(device_id)

        if device:
            device.delete_instance()
            return True
        return False

    # Rule Section
    def list_rule(self):

        rules = models.Rule.select().order_by(models.Rule.id)

        return [rule.to_client() for rule in rules]

    def get_rule(self, rule_id):

        rule = models.Rule.get_by_id(rule_id)

        if not rule:
            rule = models.Rule()

        return rule.to_client()

    def save_rule(self, data):
        id = data.get('id')
        if id:
            rule = models.Rule.get_by_id(id)
        else:
            rule = models.Rule()

        rule.label = data.get('label')
        rule.enabled = data.get('enabled') == '1'
        rule.set_conditions(data.get('conditions'))
        rule.set_action(data.get('action'))
        rule.save()

        return rule.to_client()

    def delete_rule(self, rule_id):

        rule = models.Rule.get_by_id(rule_id)

        if rule:
            rule.delete_instance()
            return True
        return False

    def list_operator(self):

        operators = utils.get_members_by_parent(operator, operator.Operator)
        result = []

        for op in operators.values():
            data = op()
            result.append({
                'key': data.key(),
                'label': str(data)
            })

        return result

    def run_rule(self, rule_id):

        run = evaluator.Evaluate(models.Rule.get_by_id(rule_id))

        return run.evaluate()

    # POC Section
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

