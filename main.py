# ----Imports and Initialization---- #


import random

import pygame
from pygame.locals import *

# import math

pygame.init()

# ----Global Variables---- #


current_res = (1280, 720)
display_surface = pygame.display.set_mode(current_res)  # todo: make compatible for multiple displays

running = True

draw_queue = {}  # The draw queue handles layers


# ----Global Functions---- #


def modify_colour(colour, increment):
    mod_colour = colour.copy()

    for value in range(0, 3):
        if not (mod_colour[value] + increment) > 255 and not (mod_colour[value] + increment) < 0:
            mod_colour[value] += increment
        elif increment > 0:
            mod_colour[value] = 255
        elif increment < 0:
            mod_colour[value] = 0

    return mod_colour


# ----Classes---- #


class Frame(pygame.Rect):
    all_frames = []

    def __init__(self, **kwargs):
        super(Frame, self).__init__((0, 0), (0, 0))

        self.position = kwargs['position']
        self.size = kwargs['size']

        self.all_frames.append(self)


class Button(pygame.Rect):
    all_buttons = []
    font = pygame.font.SysFont('ubuntumono', 16)
    font_colour = [255, 255, 255]

    def __init__(self, **kwargs):

        super(Button, self).__init__((0, 0), (0, 0))

        if 'text' in kwargs:
            self.text = self.font.render(kwargs['text'], True, self.font_colour)
        else:
            self.text = self.font.render('No Text Specified', True, self.font_colour)

        if 'position' in kwargs:
            self.x = kwargs['position'][0]
            self.y = kwargs['position'][1]
        else:
            self.x = 0
            self.y = 0

        if 'size' in kwargs:
            self.width = kwargs['size'][0]
            self.height = kwargs['size'][1]
        else:
            self.width = self.text.get_width() + 20
            self.height = self.text.get_height() + 20

        if 'colour' in kwargs:
            self.colour = kwargs['colour']
        else:
            self.colour = [125, 0, 125]

        if 'function' in kwargs:
            self.function = kwargs['function']
        else:
            self.function = None

        self.all_buttons.append(self)


# ----Instance Declarations---- #


button = Button(text='Adam\'s Button',
                position=(600, 300),
                function=True)

# ----Main Loop---- #


while running:

    for event in pygame.event.get():

        if event.type == QUIT:
            running = False

        for button in Button.all_buttons:  # todo: fix rendering of multiple buttons (use indexes from all_buttons)
            # todo: or just move the draw_queue resetting about a bit
            # todo: just set it up for functions instead because draw calls are stupid

            if button.collidepoint(pygame.mouse.get_pos()):

                draw_queue[2] = (modify_colour(button.colour, 40), button)
                draw_queue[3] = (button.colour, button.inflate(-12, -12))

                if event.type == MOUSEBUTTONDOWN:
                    draw_queue[3] = (modify_colour(button.colour, -25), button.inflate(-12, -12))

                    if button.function:
                        draw_queue[1] = [random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
                    else:
                        print('No function assigned for the \'%s\' button.' % button)

            else:
                draw_queue[2] = (modify_colour(button.colour, -20), button)
                draw_queue[3] = (button.colour, button.inflate(-12, -12))

            button_centre = (button.centerx - button.text.get_rect().centerx,
                             button.centery - button.text.get_rect().centery)

            draw_queue[4] = (button_centre, button.text)

    draw_queue_keys = sorted(draw_queue)

    # print("The draw queue keys are: %s." % draw_queue_keys)
    # print(draw_queue, "\n")

    for key in draw_queue_keys:

        if len(draw_queue[key]) == 3:  # ----------------------------------------------- IF IT'S A SURFACE FILL
            display_surface.fill(draw_queue[key])

        elif len(draw_queue[key]) == 2:

            if type(draw_queue[key][0]) == list:
                display_surface.fill(draw_queue[key][0], draw_queue[key][1])  # -------- IF IT'S A RECT FILL

            else:
                display_surface.blit(draw_queue[key][1], draw_queue[key][0])  # -------- IF IT'S A SURFACE BLIT

    draw_queue.clear()
    del draw_queue_keys[:]

    pygame.display.update()

pygame.quit()
