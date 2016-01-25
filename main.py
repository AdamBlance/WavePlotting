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

max_FPS = 60
clock = pygame.time.Clock()

draw_queue = {'display_surface': [], 'window1': [], 'window2 etc...': []}


# ----Global Functions---- #


def draw_from_queue(queue, display_surf):

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


class GUIElement(pygame.Rect):

    def __init__(self, **kwargs):

        super(GUIElement, self).__init__((0, 0), (0, 0))

        if 'position' in kwargs:
            self.x = kwargs['position'][0]
            self.y = kwargs['position'][1]
        else:
            self.x = 0
            self.y = 0

        if 'colour' in kwargs:
            self.colour = kwargs['colour']
        else:
            self.colour = [random.randint(20, 235), random.randint(20, 235), random.randint(20, 235)]

        if 'surface' in kwargs:
            self.surface = kwargs['surface']
        else:
            self.surface = 'display_surface'


class Frame(GUIElement):
    all_frames = []

    def __init__(self, **kwargs):

        super(Frame, self).__init__(**kwargs)

        self.elements = []
        if 'elements' in kwargs:
            for element in kwargs['elements']:
                self.elements.append(element)
        else:
            print('Frame \'%s\' is empty.' % self)

        if 'size' in kwargs:
            self.width = kwargs['size'][0]
            self.height = kwargs['size'][1]
        else:
            self.width = 500
            self.height = 200

        if 'stacked' in kwargs:
            self.stacked = kwargs['stacked']
        else:
            self.stacked = True

        if 'scale' in kwargs:
            self.scale = kwargs['scale']
        else:
            self.scale = True

        if 'spacing' in kwargs:
            self.spacing = kwargs['spacing']
        else:
            self.spacing = 100
            print('You should really define spacing on frame \'%s\'. Defaulted to 100.' % self)

        if 'direction' in kwargs:
            if kwargs['direction'] in ['left', 'right', 'up', 'down']:
                self.direction = kwargs['direction']
            else:
                self.direction = 'right'
                print('Incorrect direction - frame \'%s\'. Direction can be left, right, down or up.' % self)
        else:
            self.direction = 'right'
            print('You must define direction on frame \'%s\'.')

        self.all_frames.append(self)

    def reassign_element_positions(self):

        if self.direction == 'right':

            edge_of_last_object = self.left
            middle_of_last_object = self.left

            for element in self.elements:
                if (element.height > self.height) and self.scale:
                    self.height = element.height

                if self.stacked:
                    element.midleft = (edge_of_last_object + self.spacing, self.centery)
                    edge_of_last_object = element.right
                else:
                    element.center = (middle_of_last_object + self.spacing, self.centery)
                    middle_of_last_object = element.centerx

        elif self.direction == 'left':

            edge_of_last_object = self.right
            middle_of_last_object = self.right

            for element in self.elements:
                if (element.height > self.height) and self.scale:
                    self.height = element.height

                if self.stacked:
                    element.midright = (edge_of_last_object - self.spacing, self.centery)
                    edge_of_last_object = element.left
                else:
                    element.center = (middle_of_last_object - self.spacing, self.centery)
                    middle_of_last_object = element.centerx

        elif self.direction == 'up':

            edge_of_last_object = self.bottom
            middle_of_last_object = self.bottom

            for element in self.elements:
                if (element.width > self.width) and self.scale:
                    self.width = element.width

                if self.stacked:
                    element.midbottom = (self.centerx, edge_of_last_object - self.spacing)
                    edge_of_last_object = element.up
                else:
                    element.center = (self.centerx, middle_of_last_object - self.spacing)
                    middle_of_last_object = element.centery

        elif self.direction == 'down':

            edge_of_last_object = self.top
            middle_of_last_object = self.top

            for element in self.elements:
                if (element.width > self.width) and self.scale:
                    self.width = element.width

                if self.stacked:
                    element.midtop = (self.centerx, edge_of_last_object + self.spacing)
                    edge_of_last_object = element.down
                else:
                    element.center = (self.centerx, middle_of_last_object + self.spacing)
                    middle_of_last_object = element.centery

    def add_frame_to_queue(self, queue, surface):

        queue[surface].append((modify_colour(self.colour, -30), self))
        queue[surface].append((self.colour, self.inflate(-8, -8)))


class Button(GUIElement):
    all_buttons = []
    font = pygame.font.SysFont('ubuntumono', 15)
    font_colour = [255, 255, 255]

    def __init__(self, **kwargs):

        super(Button, self).__init__(**kwargs)

        if 'text' in kwargs:
            self.text = self.font.render(kwargs['text'], True, self.font_colour)
        else:
            self.text = self.font.render('No Text Specified', True, self.font_colour)

        if 'size' in kwargs:
            self.width = kwargs['size'][0]
            self.height = kwargs['size'][1]
        else:
            self.width = self.text.get_width() + 20
            self.height = self.text.get_height() + 20

        if 'function' in kwargs:
            self.function = kwargs['function']
        else:
            self.function = None

        self.all_buttons.append(self)

    def add_button_to_queue(self, queue, surface):

        # This is inefficient, but I changed it so it would be easy to debug. I'll sort it out later.

        if self.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0]:
            queue[surface].append((modify_colour(self.colour, 40), self))
            queue[surface].append((self.colour, self.inflate(-8, -8)))
            # print('hovering')

        elif self.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            queue[surface].append((modify_colour(self.colour, 40), self))
            queue[surface].append((modify_colour(self.colour, -30), self.inflate(-8, -8)))
            # print('hovering and clicking')

        else:
            queue[surface].append((modify_colour(self.colour, -30), self))
            queue[surface].append((self.colour, self.inflate(-8, -8)))
            # print('nothing')

        button_centre = (button.centerx - button.text.get_rect().centerx,
                         button.centery - button.text.get_rect().centery)
        queue[surface].append((button_centre, self.text))


# ----Instance Declarations---- #


# button = Button(text='Adam\'s Button',
#                 colour=[17, 156, 170])
#
# second_button = Button(text='Adam\'s Other Button',
#                        colour=[122, 122, 255])

keypad_button_1 = Button(text='1')
keypad_button_2 = Button(text='2')
keypad_button_3 = Button(text='3')
keypad_button_4 = Button(text='4')

# If only a single object is in a frame, pass it in a list (e.g. elements=[button])

my_frame = Frame(position=(250, 260),
                 direction='down',
                 stacked=False,
                 scale=True,
                 spacing=40,
                 size=(700, 200),
                 elements=(keypad_button_1, keypad_button_2, keypad_button_3, keypad_button_4))


# ----Main Loop---- #


# todo: Make screen clear every tick because buttons are duplicating when resizing frames

while running:

    display_surface.fill([0, 0, 0])

    for event in pygame.event.get():

        if event.type == QUIT:
            running = False

    for frame in Frame.all_frames:
        frame.reassign_element_positions()
        frame.add_frame_to_queue(draw_queue, frame.surface)

    for button in Button.all_buttons:
        button.add_button_to_queue(draw_queue, button.surface)
        # button.try_function_call()

    draw_from_queue(draw_queue, display_surface)
    pygame.display.update()

    clock.tick(max_FPS)

pygame.quit()
