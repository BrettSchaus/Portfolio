from turtle import Turtle


class Rocket(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("images/rocket_small.png")
        self.penup()
        self.y_move = 10
        self.is_fired = False

    def fire(self, x_position):
        self.showturtle()
        new_x = x_position
        new_y = self.ycor() + self.y_move
        self.goto(new_x, new_y)
        self.is_fired = True
