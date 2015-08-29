import logging

has_module = False

OUT = 1
HIGH = 2
LOW = 3

try:
    import Adafruit_BBIO.GPIO as GPIO
    import Adafruit_BBIO.ADC as ADC

    OUT = GPIO.OUT
    HIGH = GPIO.HIGH
    LOW = GPIO.LOW
    ADC.setup()
    has_module = True

except ImportError as e:
    logging.debug('Adafruit_BBIO module not found.')


__author__ = 'faisal'


acceptable_pins = ["P9_33", "P9_35", "P9_36", "P9_37", "P9_38", "P9_39", "P9_40"]


def read(pin):
    """Reads a sensor value by pin
    :param pin:
    :return:
    """
    logging.debug('Reading pin: {}'.format(pin))
    reading = -1
    if pin in acceptable_pins:
        if has_module:
            reading = ADC.read(pin)
        else:
            reading = 1
            logging.debug('Faked reading')
    else:
        logging.debug('Pin {} does not exists'.format(pin))
        reading = -2

    logging.debug('Read value: {}'.format(reading))
    return reading


def output(pin, voltage):
    """GPIO.output wrapper
    :param pin:
    :param voltage:
    :return:
    """
    logging.debug('Setting pin {} output to {}'.format(pin, voltage))

    if has_module:
        GPIO.setup(pin, OUT)
        GPIO.output(pin, voltage)

    logging.debug('Pin output adjusted')


def output_high(pin):
    """Shortcut for toggle on
    :param pin:
    :return:
    """
    output(pin, HIGH)


def output_low(pin):
    """Shortcut for toggle off
    :param pin:
    :return:
    """
    output(pin, LOW)