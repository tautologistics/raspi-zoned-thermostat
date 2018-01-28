import RPi.GPIO as gpio

class Button(object):

  pin = None

  def __init__(self, pin):
    self.pin = pin
    gpio.setmode(gpio.BCM)
    gpio.setup(self.pin, gpio.IN, pull_up_down=gpio.PUD_UP)
    gpio.add_event_detect(self.pin, gpio.RISING)

  @property
  def pressed(self):
    return gpio.event_detected(self.pin)
