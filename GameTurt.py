import turtle
import turtle as tr
import time
import random

class GameTurt():
    def __init__(self):
        self.screen = tr.Screen()
        self.countdown = 10
        self.score = GameTurt.score(self)
        self.level = GameTurt.level(self)
        self.time = GameTurt.set_timer(self)


    def set_timer(self):
        self.time = tr.Turtle()
        t = self.time
        t.hideturtle()
        t.penup()
        t.goto(-295, 235)
        self.countdown = 10

        def tick():
            t.clear()
            t.write(str(self.countdown), align='center', font=('Arial', 25, 'normal'))
            self.countdown -= 1
            if self.countdown >= 0:
                self.screen.ontimer(tick, 1000)
            else:
                self.game_over()



        tick()

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

    def game_over(self):
        gmov = tr.Turtle()
        gmov.hideturtle()
        gmov.penup()
        gmov.goto(0, 0)
        tr.clearscreen()
        gmov.write("GAME OVER", align='center', font=('Arial', 40, 'bold'))
class EnemyTurt():
    def __init__(self,color):
        self.turtle = tr.Turtle()
        self.alive = True
        self.shape = self.turtle.shape("turtle")
        self.turtle.shapesize(1.2)
        self.color = color
        self.turtle.color(color)
        self.turtle.penup()
        self.move_counter = 0 # this is here to count frames in move()


    def move(self, enemies):
        self.move_counter += 1
        if self.move_counter % 7 == 0:  # only move every 7 frames for each turtle
            self.turtle.left(random.randint(30, 280))
            self.separate(enemies) #checks distance relative to other turtles and moves away if too close
            self.bounce()
            self.turtle.forward(random.randint(20,100))
            self.separate(enemies) # checks again after moving

    def separate(self,enemies):
        for other in enemies:
            if other is not self and self.turtle.distance(other.turtle) < 80:
                angle = self.turtle.towards(other.turtle) - 180
                #this checks if the turtles distance from the self
                self.turtle.setheading(angle)
                self.turtle.forward(20)



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
        if y > 100:
            self.turtle.sety(100)
        if y < -200:
            self.turtle.sety(-200)
#class PlayerTurt():
 #   def __init__(self):
  #      self.score = 0
        #self.name = name




def main():
    tr.tracer(2) #only updates screen after every turtle has moved once
    hud = GameTurt()
    colors = ["blue","purple","red","orange","yellow","green","black"]
    enemies = []
    for color in colors:
        e = EnemyTurt(color)
        enemies.append(e)
    while True:
        for e in enemies:
            e.move(enemies)
        tr.update()
        time.sleep(0.054)


main()