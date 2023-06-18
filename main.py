######################################################################
#                             Libraries                              #
######################################################################


from pygame import Surface, init
from pygame import K_ESCAPE, QUIT, quit
from pygame import K_LEFT, K_RIGHT, K_DOWN, K_UP
from pygame import K_w, K_a, K_s, K_d

from pygame import display, event, draw
from pygame.time import Clock, get_ticks
from pygame.key import get_pressed

from random import choice
from itertools import product

from library_checker import *


######################################################################
#                             Variables                              #
######################################################################


init()
WIDTH, HEIGHT = 510, 510
screen = display.set_mode((WIDTH, HEIGHT))

display.set_caption("Python Snake")
clock = Clock()

flag = True


######################################################################
#                            Class Snake                             #
######################################################################


class Snake:
    def __init__(self, screen: Surface) -> None:
        self.screen = screen

        self.head_x, self.head_y = 255, 245
        self.snake_tail = [(255, 255), (255, 265)]
        self.direction = "up"

        self.food_coordinates = choice(
            [elem for elem in product(range(5, 515, 10), range(5, 515, 10)) if elem != (self.head_x, self.head_y) and elem not in self.snake_tail]
        )
        
        self.tact = True
        self.first_ticks = 0
        self.second_ticks = 100

    def game_restart(self) -> None:
        self.screen = screen

        self.head_x, self.head_y = 255, 245
        self.snake_tail = [(255, 255), (255, 265)]
        self.direction = "up"

        self.food_coordinates = choice(
            [elem for elem in product(range(5, 515, 10), range(5, 515, 10)) if elem != (self.head_x, self.head_y) and elem not in self.snake_tail]
        )
        
        self.tact = True
        self.first_ticks = 0
        self.second_ticks = 100

    def another_direction(self) -> None:
        keys = get_pressed()
        if (keys[K_RIGHT] or keys[K_d]) and self.direction != "left" and self.tact:
            self.direction = "right"
            self.tact = False
        elif (keys[K_LEFT] or keys[K_a]) and self.direction != "right" and self.tact:
            self.direction = "left"
            self.tact = False
        elif (keys[K_UP] or keys[K_w]) and self.direction != "down" and self.tact:
            self.direction = "up"
            self.tact = False
        elif (keys[K_DOWN] or keys[K_s]) and self.direction != "up" and self.tact:
            self.direction = "down"
            self.tact = False

    def move(self) -> None:
        if (self.head_x, self.head_y) in self.snake_tail:
            self.game_restart()
            return None

        if self.second_ticks - self.first_ticks >= 50:
            self.snake_tail[1:] = self.snake_tail[:-1]
            self.snake_tail[0] = self.head_x, self.head_y
            self.tact = True

            if self.direction == "up":
                self.head_y = (self.head_y - 10) % HEIGHT
            elif self.direction == "down":
                self.head_y = (self.head_y + 10) % HEIGHT
            elif self.direction == "left":
                self.head_x = (self.head_x - 10) % WIDTH
            elif self.direction == "right":
                self.head_x = (self.head_x + 10) % WIDTH
            
            self.first_ticks = get_ticks()
        self.second_ticks = get_ticks()
    
    def food_spawning(self) -> None:
        if (self.head_x, self.head_y) == self.food_coordinates:
            self.snake_tail.append(self.snake_tail[-1])
            self.food_coordinates = choice(
                [elem for elem in product(range(5, 515, 10), range(5, 515, 10)) if elem != (self.head_x, self.head_y) and elem not in self.snake_tail]
            )

    def screen_drawing(self) -> None:
        self.screen.fill((0, 0, 0))

        draw.rect(self.screen, (200, 200, 200), (self.head_x - 5, self.head_y - 5, 10, 10))
        draw.ellipse(self.screen, (255, 0, 0), (self.food_coordinates[0] - 5, self.food_coordinates[1] - 5, 10, 10))

        for square in self.snake_tail:
            draw.rect(self.screen, (200, 200, 200), (square[0] - 5, square[1] - 5, 10, 10))        

    def pygame_events_checker(self) -> None:
        global flag
        keys = get_pressed()
        for pygame_event in event.get():
            if pygame_event.type == QUIT or keys[K_ESCAPE]:
                flag = False


######################################################################
#                           Main Functions                           #
######################################################################


def main():
    Player = Snake(screen)

    while flag:
        clock.tick(120)

        Player.another_direction()
        Player.food_spawning()
        Player.move()
        Player.screen_drawing()
        Player.pygame_events_checker()

        display.update()


######################################################################
#                             Starting                               #
######################################################################


if __name__ == '__main__':
    main()
    quit()


######################################################################
#                  Made by: @Ice_Lightning_Strike                    #
######################################################################