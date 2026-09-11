from turtle import Turtle

STARTING_Y_POSITIONS = [40, 20, 0, -20, -40]
MOVE_DISTANCE = 40

class Block(Turtle):

    def __init__(self, position):
        super().__init__()
        self.shape("square")
        self.penup()
        self.color("white")
        self.shapesize(1, 5)
        self.goto(x=position[0], y=position[1])

    def create_block(self):
        pass