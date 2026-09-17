from turtle import Screen, Turtle
from spaceship import Spaceship
from rocket import Rocket
from scoreboard import Scoreboard
from alien import Alien
import time
import random


screen = Screen()
screen.bgcolor("black")
screen.screensize(canvwidth=800, canvheight=600)
screen.title("Space Invaders")
screen.tracer(0)

# Register shapes
screen.register_shape("images/spaceship_small.png")
screen.register_shape("images/rocket_small.png")
screen.register_shape("images/alien_small.png")

rocket = Rocket()
spaceship = Spaceship((0,-350))
scoreboard = Scoreboard()

aliens = []
last_alien_time = time.time()



screen.listen()
screen.onkey(lambda: rocket.fire(spaceship.xcor()), key="space")
screen.onkey(spaceship.left, key="Left")
screen.onkey(spaceship.right, key="Right")


game_is_on = True
while game_is_on:
    time.sleep(0.06)
    screen.update()
    
    if time.time() - last_alien_time > 2:
        alien = Alien((random.randint(-400, 400), 300))
        aliens.append(alien)
        last_alien_time = time.time()
        
    for alien in aliens:
        alien.alien_movement()
    
    if rocket.is_fired:
        rocket.fire(rocket.xcor())

    # Detect collision with rocket and alien
    for alien in aliens:
        if rocket.distance(alien) < 50:
            scoreboard.point()
            rocket.is_fired = False
            rocket.hideturtle()
            alien.hideturtle()

    # Detect collision with alien and spaceship
    for alien in aliens:
        if spaceship.distance(alien) < 50:
            game_is_on = False
            screen.write("You lose!", align="center", font=("Arial", 30, "normal"))

    # Detect when alien reaches bottom
    for alien in aliens:
        if alien.ycor() < -200:
            game_is_on = False
            screen.write("You lose!", align="center", font=("Arial", 30, "normal"))



screen.exitonclick()