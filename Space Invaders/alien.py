from turtle import Turtle


class Alien(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("images/alien_small.png")
        self.penup()
        self.x_move = 10
        self.y_move = 10

    def alien_movement(self):
        new_x = self.xcor() + self.x_move
        new_y = self.ycor()

        if new_x > 400:
            new_y = self.ycor() - self.y_move
            self.x_move = -self.x_move

        elif new_x < -400:
            new_y = self.ycor() - self.y_move
            self.x_move = -self.x_move

        self.goto(new_x, new_y)