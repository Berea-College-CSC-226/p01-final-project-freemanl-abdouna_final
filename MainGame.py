######################################################################
# Authors: Ahmed Abdoun, Leroy Freeman
# Username: freemanl, abdouna
#
# P01: Final Project
#
# Purpose: creating a main game program that uses the functions at the end of the
# boss turt and gameturt files, beating the gameturt will open the bossturt
# ######################################################################
import turtle as tr
import time
from GameTurt import run_level_one
from BossTurt import run_boss_fight


def show_title():
    screen = tr.Screen()
    screen.setup(700, 600)
    screen.bgcolor("black")

    state = {"clicked": False}

    def on_click(x, y):
        state["clicked"] = True

    t = tr.Turtle()
    t.hideturtle()
    t.penup()
    t.color("white")
    t.goto(0, 100)
    t.write("The Adventure of the Legendary Turtle Hunter", align='center', font=('Arial', 20, 'bold'))
    t.goto(0, 30)
    t.write("Seven evil turtles escaped the sanctuary.", align='center', font=('Arial', 16, 'normal'))
    t.goto(0, 0)
    t.write("Catch them all before time runs out.", align='center', font=('Arial', 16, 'normal'))
    t.goto(0, -30)
    t.write("Then face the king turtle.", align='center', font=('Arial', 16, 'normal'))
    t.goto(0, -120)
    t.write("Click anywhere to begin", align='center', font=('Arial', 20, 'italic'))

    screen.onclick(on_click)

    while not state["clicked"]:
        screen.update()
        time.sleep(0.05)

    tr.clearscreen()  # clear instead of bye() so level 1 can reuse the window


def main():
    show_title()

    result = run_level_one()

    if result == "won":
        run_boss_fight()
    else:
        print("Game over. Run again to retry.")


if __name__ == "__main__":
    main()