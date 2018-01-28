from multiprocessing import Process, Value
import os
import signal
import time

import Adafruit_DHT
from bunch import Bunch

from thermostat import create as create_thermostat
from display import Display
from button import Button

TEMPERATURE_SENSOR = Adafruit_DHT.DHT11
TEMPERATURE_PIN_A = 4
TEMPERATURE_PIN_B = 17

BUTTON_PIN_UP = 21
BUTTON_PIN_DOWN = 20

def c_to_f(celcius):
  return 9.0 / 5.0 * celcius + 32

def main():

  workers = Bunch(
    sensor_temp_a=create_thermostat(TEMPERATURE_SENSOR, TEMPERATURE_PIN_A, 2),
    sensor_temp_b=create_thermostat(TEMPERATURE_SENSOR, TEMPERATURE_PIN_B, 2),
  )

  try:

    for worker_id, worker in workers.items():
      print("Starting worker %s" % worker_id)
      worker.process.start()

    display = Display()
    button_up = Button(BUTTON_PIN_UP)
    button_down = Button(BUTTON_PIN_DOWN)

    button_count = 0
    while True:
      is_changed = workers.sensor_temp_a.changed or workers.sensor_temp_b.changed
      if button_up.pressed:
        is_changed = True
        button_count += 1
      if button_down.pressed:
        is_changed = True
        button_count -= 1
      if is_changed:
        display.write_lines([
          '#1: %.02fF :: %.02f%%' % (
            c_to_f(workers.sensor_temp_a.temperature.value),
            workers.sensor_temp_a.humidity.value,
            ),
          '#2: %.02fF :: %.02f%%' % (
            c_to_f(workers.sensor_temp_b.temperature.value),
            workers.sensor_temp_b.humidity.value,
            ),
          'Button: %d' % button_count,
          '???',
        ])

      # print({
      #   'a': {
      #     'humidity': workers.sensor_temp_a.humidity.value,
      #     'temperature': c_to_f(workers.sensor_temp_a.temperature.value),
      #   },
      #   'b': {
      #     'humidity': workers.sensor_temp_b.humidity.value,
      #     'temperature': c_to_f(workers.sensor_temp_b.temperature.value),
      #   },
      # })

      time.sleep(0.1)

  except KeyboardInterrupt:

    print('Main received ctrl-c')
    display.close()
    for worker_id, worker in workers.items():
      print("Killing worker %s" % worker_id)
      worker.process.terminate()
    for worker_id, worker in workers.items():
      worker.process.join()

if __name__ == "__main__":
  main()
