import time
from pingsensor import PingSensor

sensor = PingSensor()
sensor.setInterval(0.5)
time.sleep(5)
print("2")
sensor.setInterval(0.5)
sensor.setInterval(2)
time.sleep(10)
print("stop")
sensor.setInterval(0)

