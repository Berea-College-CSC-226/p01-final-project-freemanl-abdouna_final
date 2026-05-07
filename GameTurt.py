######################################################################
# Authors: Ahmed Abdoun, Leroy Freeman
# Username: freemanl, abdouna
#
# P01: Final Project
#
# Purpose: creating a game where seven turtles run around and the player has to catch them before
# the time runs out.
# ######################################################################
import turtle as tr
import time
import random

class GameTurt():
    def __init__(self):
        self.screen = tr.Screen()
        self.countdown = 40
        self.mini = 0
        self.maxi = 7
        self._score_turtle = None
        self._level_turtle = None
        self._time_turtle = None
        self.won = False
        self.lost = False
        self.setup_hud()


    def setup_hud(self):
        self.setup_screen()
        self._setup_timer()
        self._setup_score()
        self._setup_level()


    def setup_screen(self):
        self.screen.bgpic("image/proj_bg.gif")

    def _setup_timer(self):
        self._time_turtle = tr.Turtle()
        t = self._time_turtle
        t.hideturtle()
        t.penup()
        t.goto(-295, 235)

        def tick():
            t.clear()
            t.write(str(self.countdown), align='center', font=('Arial', 25, 'normal'))
            self.countdown -= 1
            if self.countdown >= 0:
                self.screen.ontimer(tick, 1000)
            else:
                self.game_over()

        tick()

    def _setup_score(self):
        self._score_turtle = tr.Turtle()
        l = self._score_turtle
        l.penup()
        l.hideturtle()
        l.goto(-10, 230)
        l.write(f"Score: {self.mini}/{self.maxi}", align='center', font=('Arial', 30, 'normal'))

    def _setup_level(self):
        self._level_turtle = tr.Turtle()
        d = self._level_turtle
        d.penup()
        d.hideturtle()
        d.goto(252, 230)
        d.write("Level 1", align='center', font=('Arial', 30, 'normal'))

    def update_score(self):
        """Redraws the score display."""
        self._score_turtle.clear()
        self._score_turtle.write(f"Score: {self.mini}/{self.maxi}", align='center', font=('Arial', 30, 'normal'))
        if self.mini == self.maxi:
            self.win_game()

    def game_over(self):
        self.lost = True

    def win_game(self):
        self.won = True

    def show_game_over_screen(self):
        """Shows GAME OVER. Returns retry if R pressed and returns quit if Q pressed."""
        tr.clearscreen()
        self.screen.bgcolor("black")

        msg = tr.Turtle()
        msg.hideturtle()
        msg.penup()
        msg.color("red")
        msg.goto(0, 50)
        msg.write("GAME OVER", align='center', font=('Arial', 50, 'bold'))
        msg.color("white")
        msg.goto(0, -30)
        msg.write("Press R to retry  |  Q to quit", align='center', font=('Arial', 20, 'normal'))

        choice = {"value": None}

        def on_retry():
            choice["value"] = "retry"

        def on_quit():
            choice["value"] = "quit"

        self.screen.onkeypress(on_retry, "r")
        self.screen.onkeypress(on_quit, "q")
        self.screen.listen()

        while choice["value"] is None:
            self.screen.update()
            time.sleep(0.05)

        # wipe game over screen before returning so the retry starts clean
        tr.clearscreen()
        self.screen.bgcolor("white")  # reset from black so bgpic shows correctly
        return choice["value"]

class PlayerTurt():
    """
    arrow key controlled turtle that scores a point each time it
    touches an enemy turtle.
    """
    step = 20          # pixels per key-press
    collide_dist = 25  # distance that counts as a collision

    def __init__(self, hud: GameTurt):
        self.hud = hud
        self.turtle = tr.Turtle()
        t = self.turtle
        t.shape("circle")
        t.shapesize(1.5)
        t.color("black")
        t.penup()
        t.goto(0, -50)   # start near the center of the play area

        # Bind arrow keys
        screen = hud.screen
        screen.listen()
        screen.onkeypress(self.move_up,    "Up")
        screen.onkeypress(self.move_down,  "Down")
        screen.onkeypress(self.move_left,  "Left")
        screen.onkeypress(self.move_right, "Right")

    # movement
    def move_up(self):
        y = self.turtle.ycor()
        if y < 100:
            self.turtle.sety(y + self.step)

    def move_down(self):
        y = self.turtle.ycor()
        if y > -200:
            self.turtle.sety(y - self.step)

    def move_left(self):
        x = self.turtle.xcor()
        if x > -275:
            self.turtle.setx(x - self.step)

    def move_right(self):
        x = self.turtle.xcor()
        if x < 275:
            self.turtle.setx(x + self.step)

    # collision detection
    def check_collisions(self, enemies: list):
        """
        check collisions every frame and hide the turtle if its caught
        """
        for enemy in enemies:
            if enemy.alive and self.turtle.distance(enemy.turtle) < self.collide_dist:
                enemy.turtle.hideturtle()
                enemy.alive = False
                self.hud.mini += 1
                self.hud.update_score()


class EnemyTurt():
    def __init__(self, color):
        self.turtle = tr.Turtle()
        self.alive = True
        self.turtle.shape("turtle")
        self.turtle.shapesize(1.2)
        self.color = color
        self.turtle.color(color)
        self.turtle.penup()
        self.move_counter = 0

    def move(self, enemies):
        if not self.alive:
            return
        self.move_counter += 1
        if self.move_counter % 7 == 0:
            self.turtle.left(random.randint(30, 280))
            self.separate(enemies)
            self.bounce()
            self.turtle.forward(random.randint(20, 100))
            self.separate(enemies)

    def separate(self, enemies):
        for other in enemies:
            if other is not self and other.alive and self.turtle.distance(other.turtle) < 80:
                angle = self.turtle.towards(other.turtle) - 180
                self.turtle.setheading(angle)
                self.turtle.forward(20)

    def bounce(self):
        x = self.turtle.xcor()
        y = self.turtle.ycor()
        if x > 300:
            self.turtle.setx(275)
        if x < -275:
            self.turtle.setx(-275)
        if y > 100:
            self.turtle.sety(100)
        if y < -200:
            self.turtle.sety(-200)


def run_level_one():
    while True:
        tr.tracer(2)
        hud = GameTurt()
        colors = ["blue", "purple", "red", "orange", "yellow", "brown", "cyan"]
        enemies = [EnemyTurt(c) for c in colors]
        player = PlayerTurt(hud)

        while not hud.won and not hud.lost:
            for e in enemies:
                e.move(enemies)
            player.check_collisions(enemies)
            tr.update()
            time.sleep(0.054)

        if hud.won:
            tr.bye()
            return "won"

        choice = hud.show_game_over_screen()
        if choice == "quit":
            tr.bye()
            return "quit"



if __name__ == "__main__":
    run_level_one()