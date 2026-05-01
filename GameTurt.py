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
        self.setup_hud()

    def setup_hud(self):
        self._setup_timer()
        self._setup_score()
        self._setup_level()

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

    def game_over(self):
        tr.clearscreen()
        gmov = tr.Turtle()
        gmov.hideturtle()
        gmov.penup()
        gmov.goto(0, 0)
        gmov.write("GAME OVER", align='center', font=('Arial', 40, 'bold'))


class PlayerTurt():
    """
    Arrow-key controlled turtle that scores a point each time it
    touches an enemy turtle.  Once an enemy is caught it is hidden
    and marked dead so it can't be scored again.
    """
    STEP = 20          # pixels per key-press
    COLLIDE_DIST = 25  # distance (px) that counts as a collision

    def __init__(self, hud: GameTurt):
        self.hud = hud
        self.turtle = tr.Turtle()
        t = self.turtle
        t.shape("turtle")
        t.shapesize(1.5)
        t.color("black")
        t.penup()
        t.goto(0, -50)   # start near the centre of the play area

        # Bind arrow keys
        screen = hud.screen
        screen.listen()
        screen.onkeypress(self.move_up,    "Up")
        screen.onkeypress(self.move_down,  "Down")
        screen.onkeypress(self.move_left,  "Left")
        screen.onkeypress(self.move_right, "Right")

    # ── movement ──────────────────────────────────────────────────────────
    def move_up(self):
        y = self.turtle.ycor()
        if y < 100:
            self.turtle.sety(y + self.STEP)

    def move_down(self):
        y = self.turtle.ycor()
        if y > -200:
            self.turtle.sety(y - self.STEP)

    def move_left(self):
        x = self.turtle.xcor()
        if x > -275:
            self.turtle.setx(x - self.STEP)

    def move_right(self):
        x = self.turtle.xcor()
        if x < 275:
            self.turtle.setx(x + self.STEP)

    # ── collision detection ───────────────────────────────────────────────
    def check_collisions(self, enemies: list):
        """
        Call once per game loop frame.  For every still-alive enemy
        within COLLIDE_DIST, hide it, mark it dead, and add a point.
        """
        for enemy in enemies:
            if enemy.alive and self.turtle.distance(enemy.turtle) < self.COLLIDE_DIST:
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


def main():
    tr.tracer(2)
    hud = GameTurt()

    colors = ["blue", "purple", "red", "orange", "yellow", "green", "black"]
    enemies = [EnemyTurt(c) for c in colors]

    player = PlayerTurt(hud)

    while True:
        for e in enemies:
            e.move(enemies)
        player.check_collisions(enemies)
        tr.update()
        time.sleep(0.054)


main()