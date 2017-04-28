from threading import Event
from threading import Thread
 
class RepeatTimer(object):

    def __init__(self):
        self.stopEvent = Event()
 
    def start(self, interval, callback):
        self.stopEvent.set()
        self.interval = interval
        self.callback = callback
        self.stopEvent = Event()
        RepeatTimer.TimerThread(self).start()
 
    def stop(self):
        self.stopEvent.set()
 
    class TimerThread(Thread):
        def __init__(self, timer):
            Thread.__init__(self)
            self.timer = timer
            self.setDaemon(True)
 
        def run(self):
            while not self.timer.stopEvent.wait(self.timer.interval):
                self.timer.callback()