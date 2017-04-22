import time
from pingsensor import PingSensor
from repeat_timer import RepeatTimer

class LEDShow(object):

    distance = 0

    def __init__(self):
        sensor = PingSensor(self.setDistance)
        sensor.setInterval(0.5)
        time.sleep(5)
        print("2")
        sensor.setInterval(2)
        time.sleep(10)
        sensor.setInterval(0)

    def setDistance(self, d):
        distance = d
        print("distance: "+str(distance))
