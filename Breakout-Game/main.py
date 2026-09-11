from turtle import Screen
from paddle import Paddle
from ball import Ball
from blocks import Block
from scoreboard import Scoreboard
import time


screen = Screen()
screen.bgcolor("black")
screen.screensize(canvwidth=800, canvheight=600)
screen.title("Breakout")
screen.tracer(0)

paddle = Paddle((0,-350))
for i in range(8):
    for j in range (5):
        blocks = Block((-360 + i * 105, 180 + j * 40))
ball = Ball()
scoreboard = Scoreboard()

screen.listen()
screen.onkey(paddle.left, key="Left")
screen.onkey(paddle.right, key="Right")


game_is_on = True
while game_is_on:
    time.sleep(ball.move_speed)
    screen.update()
    ball.move_ball()

    # Detect collision with top wall
    if ball.ycor() > 380:
        ball.bounce_y()

    # Detect collision with left or right wall
    if ball.xcor() > 450 or ball.xcor() < -450:
        ball.bounce_x()


    # Detect when paddle misses
    if ball.ycor() < -400:
        ball.reset_position()
        scoreboard.point()


screen.exitonclick()