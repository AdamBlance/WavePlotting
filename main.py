"""
Adam Blance, Dec 2015 - 2016
main.py
"""

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

"""
The draw queue draws objects based on which surface they should be blitted to.
Surface lists are housed within the queue that contain the functions used to draw GUI elements.
"""

draw_queue = {'display_surface': [], 'window1': [], 'window2 etc...': []}


# ----Global Functions---- #


def draw_from_queue(queue, display_surf, **kwargs):
    for surface in queue:
        if surface == 'display_surface':
            for draw_call in queue[surface]:
                if len(draw_call) == 2:
                    if type(draw_call[0]) == list:
                        display_surf.fill(draw_call[0], draw_call[1])  # This is a rect fill call
                    else:
                        display_surf.blit(draw_call[1], draw_call[0])  # This is a blit to a surface
                else:
                    display_surf.fill(draw_call[0])  # This is a surface fill

        del queue[surface][:]


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


# todo: Make frames scale to button size if requested by user


class Frame(pygame.Rect):
    all_frames = []

    def __init__(self, **kwargs):

        super(Frame, self).__init__((0, 0), (0, 0))

        if 'stacked' in kwargs:
            self.stacked = kwargs['stacked']
        else:
            self.stacked = True
        if 'scale' in kwargs:
            self.scale = kwargs['scale']
        else:
            self.scale = True
        if 'position' in kwargs:
            self.position = kwargs['position']
        else:
            self.position = (0, 0)

        if 'elements' in kwargs:
            for element in kwargs['elements']:
                self.elements.append(element)
        else:
            print('Frame \'%s\' is empty.' % self)

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
            self.colour = [random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)]
        if 'function' in kwargs:
            self.function = kwargs['function']
        else:
            self.function = None

        self.surface = kwargs['surface']

        self.all_buttons.append(self)

    def add_button_to_queue(self, queue, surface):

        if self.collidepoint(pygame.mouse.get_pos()):
            if not pygame.mouse.get_pressed()[0]:
                queue[surface].append((modify_colour(self.colour, 40), self))
                queue[surface].append((self.colour, self.inflate(-12, -12)))
            else:
                queue[surface].append((modify_colour(self.colour, 40), self.inflate(-12, -12)))
                queue[surface].append((modify_colour(self.colour, -30), self.inflate(-12, -12)))
        else:
            queue[surface].append((modify_colour(self.colour, -30), self))
            queue[surface].append((self.colour, self.inflate(-12, -12)))

        button_centre = (button.centerx - button.text.get_rect().centerx,
                         button.centery - button.text.get_rect().centery)
        queue[surface].append((button_centre, self.text))


# ----Instance Declarations---- #


"""
The "surface" specified when creating GUI elements can either be a frame or a surface.
If an object is part of a frame, it's current position will be overwritten by the frame (if one is specified).
If the object is not part of a frame, it will be placed on the specified surface with the co-ords defined.
Frame definitions should come before GUI elements housed inside them.
"""


button = Button(text='Adam\'s Button',
                colour=[17, 156, 170],
                surface='display_surface')

my_frame = Frame(position=(200, 200),
                 stacked=True,
                 scale=True)


# ----Main Loop---- #


while running:

    for event in pygame.event.get():

        if event.type == QUIT:
            running = False

        for frame in Frame.all_frames:
            pass

        for button in Button.all_buttons:
            button.add_button_to_queue(draw_queue, button.surface)
            # button.try_function_call()

    draw_from_queue(draw_queue, display_surface)

    pygame.display.update()

pygame.quit()
