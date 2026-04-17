import turtle
import turtle as tr
import time

class GameTurt():
    def __init__(self):
        self.screen = tr.Screen()
        self.score = GameTurt.score(self)
        self.level = GameTurt.level(self)
        self.time = GameTurt.set_timer(self)



    def set_timer(self):
        self.time = tr.Turtle()
        t = self.time
        t.hideturtle()
        t.penup()
        t.goto(-295,235)
        v = "30"
        for i in range(30):
            t.write(v, align= 'center', font=('Arial', 25, 'normal'))
            v = int(v)
            v = v - 1
            v = str(v)
            time.sleep(1)
            t.clear()

    def score(self):
        self.score = tr.Turtle()
        l = self.score
        l.pu()
        l.hideturtle()
        l.goto(-10,230)
        mini = 0
        maxi = 7
        l.write(f"Score: {mini}/{maxi}", align= 'center', font= ('Arial', 30, 'normal'))

    def level(self):
        self.level = tr.Turtle()
        d = self.level
        d.penup()
        d.hideturtle()
        d.goto(252,230)
        d.write("Level 1", align= 'center', font=('Arial',30,'normal'))

class RunningTurt():
    def __init__(self,color):
        self.turtle = tr.Turtle
        self.alive = True
        self.shape = self.turtle.shape("turtle")
        self.color = color
        self.turtle.color(color)


screen = GameTurt()
