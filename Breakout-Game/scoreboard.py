from turtle import Turtle

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.lives = 3
        self.update_scoreboard()

    def update_scoreboard(self):
        self.clear()
        self.goto(-400, -350)
        self.write(f"Score: {self.score}", align="center", font=("Courier", 20, "normal"))

        self.goto(350, -350)
        self.write(f"Lives left: {self.lives}", align="center", font=("Courier", 20, "normal"))

    def lost_life(self):
        self.lives -= 1
        self.update_scoreboard()

    def point(self):
        self.score += 1
        self.update_scoreboard()

    def game_over(self):
        self.goto(0, 50)
        self.write("GAME OVER",
                   align="center",
                   font=("Courier", 60, "normal"))

        self.goto(0, -50)
        self.write(f"Score: {self.score}",
                   align="center",
                   font=("Courier", 40, "normal"))
    def game_won(self):
        self.goto(0, 50)
        self.write("YOU WON!",
                   align="center",
                   font=("Courier", 60, "normal"))

        self.goto(0, -50)
        self.write(f"Score: {self.score}",
                   align="center",
                   font=("Courier", 40, "normal"))