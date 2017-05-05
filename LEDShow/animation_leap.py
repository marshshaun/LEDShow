from _animation import Animation
import time
import utils

class AnimationLeap(Animation):

    def __init__(self):
        self._running = False
        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

    def run(self, leds):
       self._running = True

       rowCount = leds.getRowCount() - 2
       self.interval = int(rowCount/6)
       
       c = 0
       self.rows = []
       for row in range(self.interval, rowCount+self.interval, self.interval):
           self.rows.append(row)
           self.drawSquare(leds, 0, row, self.colors[c])
           c += 1
           leds.show()

       self.swap(leds, 0, 1)
       self.swap(leds, 1, 2)
       self.swap(leds, 2, 3)

       self._running = False

    def stop(self):
        self._running = False
       
    def running(self):
        return self._running             

    def pingInterval(self):
        return 1

    def pingLoop(self):
        return False

    def drawSquare(self, leds, x, y, c):
        for w in range(8):
            for h in range(self.interval):
                leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])                                 

    def clearSquare(self, leds, x, y, c):
        for w in range(8):
            for h in range(self.interval):
                leds.setPixelColorXY(x+w, y-h, c[0], c[1], c[2])

    def swap(self, leds, a, b):
        r1 = self.rows[a]
        r2 = self.rows[b]
        direction = 1 if r2 > r1 else -1

        for i in range(r1, r2+direction, direction):
            self.clearSquare(leds, 0, r1, (0,0,0)) 
            self.drawSquare(leds, 0, i+direction, self.colors[a])           
            leds.show()
            time.sleep(0.05)                    

        for j in range(r2, r1-direction, -direction):
            self.clearSquare(leds, 0, r2, self.colors[a])
            self.drawSquare(leds, 0, j-direction, self.colors[b])
            leds.show()
            time.sleep(0.05)

        tmp = self.colors[a]
        self.colors[a] = self.colors[b]
        self.colors[b] = tmp
    