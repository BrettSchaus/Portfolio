import turtle
from turtle import Screen
from paddle import Paddle
from ball import Ball
from blocks import Block
from scoreboard import Scoreboard
import time

colours = ['red', 'green', 'yellow']
blocks = []

screen = Screen()
screen.bgcolor("black")
screen.screensize(canvwidth=1000, canvheight=800)
screen.title("Breakout")
screen.tracer(0)

paddle = Paddle((0,-350))
for j in range (1): # 6
    if j % 2 == 0:
        colour = colours[j // 2]

    for i in range (1): # 8
        block = Block((-370 + i * 105, 150 + j * 40))
        block.color(colour)
        blocks.append(block)

total_blocks = len(blocks)
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
        scoreboard.lost_life()

        if scoreboard.lives == 0:
            game_is_on = False
            scoreboard.game_over()
        else:
            ball.reset_position()


    # Detect collision with paddle
    if ball.distance(paddle) < 50 and ball.ycor() < -200 and ball.y_move < 0:
        ball.bounce_y()

    # Checking for collisions with blocks
    for block in blocks:
        if ball.distance(block) < 50:
            block.hideturtle()
            blocks.remove(block)
            ball.bounce_y()
            scoreboard.point()
            if scoreboard.score == total_blocks:
                scoreboard.game_won()
                game_is_on = False
            break


screen.exitonclick()