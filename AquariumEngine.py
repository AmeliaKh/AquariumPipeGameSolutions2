# import all of the necessary libraries
import random
import sys, pygame
import os
from pygame.locals import *
import AquariumGraphics

PROB_FOOD = 0.1

class Food():
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos
        self.radius = 15

    def move_down(self, distance):
        self.y += distance

class PoisonousFood(Food):
    def __init__(self, x_pos, y_pos):
        super().__init__(x_pos, y_pos)

    def move_down(self, distance):
        self.y += distance * 2

class Pipe():
    def __init__(self):
        self.x = 100
        self.y = 100
        self.diameter = 70
        # list of Food objects which have been added to this pipe
        self.food_pieces = []
        self.speed = 7
        self.percentage_of_poisonous_food = 0.2

    def add_food(self):
        rand = random.uniform(0, 1)
        if rand < self.percentage_of_poisonous_food:
            food = PoisonousFood(self.x + self.diameter / 2, 0)
        else:
            food = Food(self.x + self.diameter / 2, 0)
        self.food_pieces.append(food)

    def move_food(self, boundary_y):
        for food in self.food_pieces:
            food.move_down(self.speed)
            if food.y - food.radius > boundary_y:
                self.food_pieces.remove(food)

    def check_for_eaten(self, player):
        count = 0
        for food in self.food_pieces:
            if food.y + food.radius >= player.y\
                and food.y - food.radius <= player.y + player.height\
                and food.x + food.radius >= player.x\
                and food.x - food.radius <= player.x + player.width:
                self.food_pieces.remove(food)
                if isinstance(food, PoisonousFood):
                    count -= 1
                else:
                    count += 1
        return count


class Fish(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, aquarium_width):
        pygame.sprite.Sprite.__init__(self)
        self.x = x_pos
        self.y = y_pos
        self.aquarium_width = aquarium_width
        self.speed = 10

        self.height = 60
        self.width = 70

        # Load image for player
        # (you can open the image in the assets folder to see what it looks like)
        image_left_unscaled = pygame.image.load(os.path.join("assets", "goldfish_left.png"))
        image_right_unscaled = pygame.image.load(os.path.join("assets", "goldfish_right.png"))

        # Scale the player's character to the specified height and width
        self.image_left = pygame.transform.rotate(pygame.transform.scale(
            image_left_unscaled, (self.width, self.height)), 0)
        self.image_right = pygame.transform.rotate(pygame.transform.scale(
            image_right_unscaled, (self.width, self.height)), 0)

        self.rect = self.image_left.get_rect()
        self.image = self.image_left

    def handle_movement(self, keys_pressed):
        """
        Update player's position according to the key pressed
        """
        if keys_pressed[pygame.K_LEFT] and self.x - self.speed - AquariumGraphics.border_width/2 > AquariumGraphics.offset_canvas:  # LEFT
            self.x -= self.speed
            self.image = self.image_left
        elif keys_pressed[pygame.K_RIGHT] and self.x + self.speed + self.width + AquariumGraphics.border_width/2 \
            < self.aquarium_width + AquariumGraphics.offset_canvas:  # RIGHT
            self.x += self.speed
            self.image = self.image_right
        else:
            return
        self.rect.x = self.x


class Aquarium():
    def __init__(self, width=580, height=520):
        ## initialise pygame
        pygame.init()
        pygame.font.init()

        self.score = 0
        self.game_running = True

        ## game constants
        self.width = width
        self.height = height

        ## player (the fish)
        self.player = Fish(x_pos=self.width / 2,
                           y_pos=self.height-60,
                           aquarium_width=self.width)

        ## pipe
        self.pipe = Pipe()

        ## interface
        self.DISPLAY = AquariumGraphics.setup_display(self.width, self.height)

        ## draw initial board
        self.draw()

    def draw(self):
        # A wrapper around the `AquariumGraphics.draw_board` function that picks all
        # the right components of `self`.
        AquariumGraphics.draw_board(self.DISPLAY, self.width, self.height, self.score,
                                    self.game_running, self.player, self.pipe)

    def game_loop(self):
        while self.game_running:
            # add food 2% of the time
            rand = random.uniform(0, 1)
            if rand < PROB_FOOD:
                self.pipe.add_food()

            # Process all events
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)

            # Check which key has been pressed (if any) and move player accordingly
            keys_pressed = pygame.key.get_pressed()
            self.player.handle_movement(keys_pressed)

            # Move food down pipe
            self.pipe.move_food(boundary_y=self.height)
            self.score += self.pipe.check_for_eaten(self.player)

            # Refresh the display and loop back
            self.draw()
            pygame.display.update()

            pygame.time.wait(40)

        # Once the game is finished, print the user's score and wait for the `QUIT` event.
        # Note: in its current form, this game doesn't end without the user closing the application
        # since the player can't lose. However, if you extend the game to enable the player to lose,
        # the following code will be useful.
        print('SCORE:  ', self.score)
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            pygame.time.wait(40)
