"""
Adam Blance, Dec 2015 - 2016
main.py
"""


# ----Imports and Initialization---- #


import math

from pygame.locals import *

from Surface import *
from Frame import *
from Button import *
from Wave import *


# ----Variables---- #


current_res = (1280, 720)
display_surface = pygame.display.set_mode(current_res)  # todo: implement scaling for monitors of different resolutions

running = True

max_FPS = 60
clock = pygame.time.Clock()


# ----Functions---- #


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


# ----Instance Declarations---- #

keypad_button_1 = Button(text='1')
keypad_button_2 = Button(text='2')
keypad_button_3 = Button(text='3')
keypad_button_4 = Button(text='4')

keypad_frame = Frame(position=(250, 260),
                     direction='down',
                     stacked=True,
                     spacing=10,
                     scale=False,
                     size=(700, 200),
                     elements=(keypad_button_1, keypad_button_2, keypad_button_3, keypad_button_4))

# keypad_button_1 = Button(text='1')
# keypad_button_2 = Button(text='2')
# keypad_button_3 = Button(text='3')
# keypad_button_4 = Button(text='4')
# keypad_button_5 = Button(text='5')
# keypad_button_6 = Button(text='6')
# keypad_button_7 = Button(text='7')
# keypad_button_8 = Button(text='8')
# keypad_button_9 = Button(text='9')
#
# keypad_lane_1 = Frame(direction='down',
#                       stacked=False,
#                       scale=False,
#                       spacing=40,
#                       size=(80, 300),
#                       elements=(keypad_button_1, keypad_button_4, keypad_button_7))
#
# keypad_lane_2 = Frame(direction='down',
#                       stacked=False,
#                       scale=False,
#                       spacing=40,
#                       size=(80, 300),
#                       elements=(keypad_button_2, keypad_button_5, keypad_button_8))
#
# keypad_lane_3 = Frame(direction='down',
#                       stacked=False,
#                       scale=False,
#                       spacing=40,
#                       size=(80, 300),
#                       elements=(keypad_button_3, keypad_button_6, keypad_button_9))
#
# housing_frame = Frame(position=(250, 260),
#                       direction='left',
#                       stacked=True,
#                       scale=False,
#                       size=(700, 200),
#                       elements=(keypad_lane_1, keypad_lane_2, keypad_lane_3))

main_surface = Surface([keypad_frame], (1280, 720))


# ----Main Loop---- #


while running:

    display_surface.fill([0, 0, 0])

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    for frame in Frame.all_frames:
        frame.reassign_element_positions()

    for surface in Surface.all_surfaces:
        for element in surface.get_elements():

            if isinstance(element, Button):
                element.render_button(surface)

            if isinstance(element, Frame):
                for frame_element in element.get_elements():  #  Have to allow frames to be stacked inside of frames
                    frame_element.render_button(surface)

    display_surface.blit(main_surface, (0, 0))
    pygame.display.update()

    clock.tick(max_FPS)

pygame.quit()
