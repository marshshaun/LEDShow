import time
from pingsensor import PingSensor
from repeat_timer import RepeatTimer

class LEDShow(object):

    def __init__(self):
        sensor = PingSensor()
        sensor.setInterval(0.5)
        time.sleep(5)
        print("2")
        sensor.setInterval(2)
        time.sleep(10)
        sensor.setInterval(0)

    def callback(self):
        print("callback yes")
