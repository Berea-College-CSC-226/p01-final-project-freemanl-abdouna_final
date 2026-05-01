import turtle
import turtle as tr
import time
import random

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

class EnemyTurt():
    def __init__(self,color):
        self.turtle = tr.Turtle()
        self.alive = True
        self.shape = self.turtle.shape("turtle")
        self.color = color
        self.turtle.color(color)
        self.turtle.penup()
        self.move_counter = 0 # this is here to count frames in move()

    def move(self):
        self.move_counter += 1
        if self.move_counter % 7 == 0:  # only move every 7 frames for each turtle
            self.turtle.left(random.randint(30, 280))
            self.bounce()
            self.turtle.forward(random.randint(20,100))


    def bounce(self):
        """
        this method ensures that none of the turtles will go off screen.
        if the turtle leaves the bounds it will be moved back to the edge of the
        screen
        """

        x = self.turtle.xcor()
        y = self.turtle.ycor()

        if x > 300:
            self.turtle.setx(300)
        if x < -300:
            self.turtle.setx(-300)
        if y > 200:
            self.turtle.sety(200)
        if y < -200:
            self.turtle.sety(-200)




def main():
    tr.tracer(2) #only updates screen after every turtle has moved once
    colors = ["blue","purple","red","orange","yellow","green","black"]
    enemies = []
    for color in colors:
        e = EnemyTurt(color)
        enemies.append(e)
    while True:
        for e in enemies:
            e.move()
        tr.update()
        time.sleep(0.054)
main()