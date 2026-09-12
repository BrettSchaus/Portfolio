from turtle import Turtle

STARTING_Y_POSITIONS = [40, 20, 0, -20, -40]
RIGHT_X = 350
MOVE_DISTANCE = 40
UP = 90
DOWN = 270

class Paddle(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.penup()
        self.color("white")
        self.shapesize(1, 5)
        self.goto(x=position[0], y=position[1])

    def left(self):
        new_x = self.xcor() - MOVE_DISTANCE

        if new_x < -400:
            new_x = -400

        self.goto(new_x, self.ycor())

    def right(self):
        new_x = self.xcor() + MOVE_DISTANCE

        if new_x > 400:
            new_x = 400

        self.goto(new_x, self.ycor())