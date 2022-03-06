import pygame

# This module takes care of the graphical interface: drawing the shapes and
# printing the text that together make the game window.

# display constants (these are not crucial to the game or pygame)
import AquariumEngine

fontsize = 24
offset_canvas = 24
top_offset = 24
bottom_spacing = 64
border_width = 10

# colour constants
BORDER_COLOUR = (13, 161, 146)  # dark blue
CREAM = (242, 235, 211)
BACKGROUND_COLOUR = (19, 189, 172)  # bluish
WHITE = (255,255,255)
PIPE_COLOUR = (131, 214, 206)
FOOD_COLOUR = (13, 161, 146)  # dark blue
POISONOUS_FOOD_COLOUR = (250, 101, 90)  # dark blue


def setup_display(field_width, field_height):
    window_width = 2 * offset_canvas + field_width
    window_height = 2 * offset_canvas + top_offset + bottom_spacing + field_height
    display = pygame.display.set_mode((window_width, window_height), 0, 32)
    pygame.display.set_caption('Aquarium Game')
    gamefont = pygame.font.Font(None, fontsize)
    return (display, gamefont)


# def draw_player(game_display, player):

def draw_board(
    game_display,
    field_width,
    field_height,
    score,
    game_running,
    player,
    pipe,
):
    (display, gamefont) = game_display
    display.fill(BACKGROUND_COLOUR)

    # draw all food
    for food_item in pipe.food_pieces:
        if isinstance(food_item, AquariumEngine.PoisonousFood):
            food_colour = POISONOUS_FOOD_COLOUR
        else:
            food_colour = FOOD_COLOUR
        pygame.draw.circle(display, food_colour, (food_item.x, food_item.y),
                           food_item.radius, 0)

    # draw over food overlapping border
    pygame.draw.rect(display, BACKGROUND_COLOUR,
                     (offset_canvas,
                      top_offset + field_height,
                      field_width,
                      50)
                     )

    pygame.draw.rect(display, BACKGROUND_COLOUR,
                     (offset_canvas,
                      0,
                      field_width,
                      top_offset)
                     )

    # display players' score
    score_surf = gamefont.render('SCORE: ' + str(score), False, CREAM)
    score_x = offset_canvas
    score_y = 2 * offset_canvas + top_offset + field_height
    display.blit(score_surf, (score_x, score_y))

    # display pipe
    pygame.draw.rect(display, PIPE_COLOUR, (pipe.x, pipe.y, pipe.diameter, 330))

    # display player
    display.blit(player.image, (player.x, player.y))

    # draw border
    pygame.draw.rect(display, BORDER_COLOUR,
                     (offset_canvas,
                      top_offset,
                      field_width,
                      field_height
                      ),
                     border_width)

    if not (game_running):
        draw_winners(display, gamefont, winner)


def draw_score(display, gamefont, winner):
    if winner == 0:
        win_surf = gamefont.render("DRAW!", False, BORDER_COLOUR)
    elif winner == 1:
        win_surf = gamefont.render("WHITE WINS!", False, CREAM)
    else:
        win_surf = gamefont.render("BROWN WINS!", False, BLUE)
    display.blit(win_surf, (offset_canvas, offset_canvas / 2))