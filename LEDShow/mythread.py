from threading import Thread

class MyThread(Thread):
    def __init__(self, event, interval, callback):
        Thread.__init__(self)
        self.stopped = event
        self.interval = interval
        self.callback = callback
        self.daemon = True

    def run(self):
        while not self.stopped.wait(self.interval):
            self.callback()