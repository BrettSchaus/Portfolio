from turtle import Turtle

class Spaceship(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("images/spaceship_small.png")
        self.shapesize(0.25, 0.25)
        self.penup()
        self.goto(position)
        self.move_distance = 20


    def right(self):
        new_x = self.xcor() + self.move_distance
        self.goto(new_x, self.ycor())

    def left(self):
        new_x = self.xcor() - self.move_distance
        self.goto(new_x, self.ycor())