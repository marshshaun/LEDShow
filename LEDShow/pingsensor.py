import RPi.GPIO as GPIO
import time
from repeat_timer import RepeatTimer

class PingSensor(object):

    def __init__(self):
        self.interval = 0
        self.timer = RepeatTimer()

    def ping(self):
        try:
            GPIO.setmode(GPIO.BOARD)
            GPIO.setup(11, GPIO.OUT)
            # Set to low
            GPIO.output(11, False)

            # Sleep 2 micro-seconds
            time.sleep(0.000002)

            # Set high
            GPIO.output(11, True)

            # Sleep 5 micro-seconds
            time.sleep(0.000005)

            # Set low
            GPIO.output(11, False)

            # Set to input
            GPIO.setup(11, GPIO.IN)

            # Count microseconds that SIG was high
            while GPIO.input(11) == 0:
                starttime = time.time()

            while GPIO.input(11) == 1:
                endtime = time.time()

            duration = endtime - starttime
            # The speed of sound is 340 m/s or 29 microseconds per centimeter.
            # The ping travels out and back, so to find the distance of the
            # object we take half of the distance travelled.
            # distance = duration / 29 / 2
            distance = duration * 34000 / 2
            print (str(distance)+"cm")
        finally:
            GPIO.cleanup()

    def setInterval(self, interval, pin=11):
        if(interval <= 0):
            self.interval = 0
            self.timer.stop()
            return
        if(interval != self.interval):
            self.interval = interval
            self.timer.start(self.interval, self.ping)

