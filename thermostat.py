from multiprocessing import Process, Value
import signal
import sys
import time

import Adafruit_DHT
from bunch import Bunch

def create(sensor, pin, sleep=1):

  def worker_func(sensor, pin, humidity, temperature, sleep):

    state = { 'run': True }

    def term_func(signum, frame):
      print("temperature_worker %s STOPPING %s" % (pin, signum,))
      # TODO: cleanup here
      state['run'] = False
      # sys.exit(0)

    signal.signal(signal.SIGINT, term_func)
    signal.signal(signal.SIGTERM, term_func)

    while state['run']:
      result = Adafruit_DHT.read_retry(sensor, pin)
      print("temperature_worker %s RESULT %s %s" % (pin, result[0], result[1],))
      if result and result[0] != None and result[1] != None:
        humidity.value = result[0]
        temperature.value = result[1]
      time.sleep(sleep)


  humidity = Value('d', 0.0)
  last_humidity = 0
  temperature = Value('d', 0.0)
  last_temperature = 0

  def changed():
    is_changed = False
    if last_humidity != humidity.value:
      is_changed = True
      last_humidity = humidity.value
    if last_temperature != temperature.value:
      is_changed = True
      last_temperature = temperature.value
    return is_changed

  worker = Bunch(
    process=Process(target=worker_func, args=(sensor, pin, humidity, temperature, sleep,)),
    humidity=humidity,
    temperature=temperature,
    changed=changed,
  )
  worker.process.daemon = True

  return worker
