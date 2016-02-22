"""
Adam Blance, Dec 2015 - 2016
main.py
"""


# ----Imports and Initialization---- #


from pygame.locals import *

from Surface import *
from Frame import *
from Button import *


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


for i in range(1, 10):
    exec('keypad_button_%s = Button(text="%s")' % (i, i))

keypad_lane_1 = Frame(direction='down',
                      stacked=True,
                      spacing=10,
                      colour=(255, 255, 0),
                      size=(keypad_button_1.width, keypad_button_1.height * 3 + 20),
                      elements=(keypad_button_1, keypad_button_4, keypad_button_7))

keypad_lane_2 = Frame(direction='down',
                      stacked=True,
                      spacing=10,
                      colour=(255, 255, 0),
                      size=keypad_lane_1.size,
                      elements=(keypad_button_2, keypad_button_5, keypad_button_8))

keypad_lane_3 = Frame(direction='down',
                      stacked=True,
                      spacing=10,
                      colour=(255, 255, 0),
                      size=keypad_lane_1.size,
                      elements=(keypad_button_3, keypad_button_6, keypad_button_9))

housing_frame = Frame(position=((current_res[0]/2) - 100, (current_res[1]/2) - 100),
                      direction='right',
                      stacked=True,
                      spacing=10,
                      size=(keypad_lane_1.width * 3 + 20, keypad_lane_1.height),
                      elements=(keypad_lane_1, keypad_lane_2, keypad_lane_3))

main_surface = Surface([housing_frame], current_res)


# ----Main Loop---- #


count = 0
while running:

    main_surface.fill([0, 0, 0])

    count += 1
    if count < 3:
        for frame in Frame.all_frames:
            frame.reassign_element_positions()

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    for surface in Surface.all_surfaces:   # todo: Implement infinite recursion (somehow)
        for element in surface.get_elements():

            if isinstance(element, Button):
                element.render_button(surface)

            elif isinstance(element, Frame):
                for frame_element_1 in element.get_elements():

                    if isinstance(frame_element_1, Button):
                        frame_element_1.render_button(surface)

                    elif isinstance(frame_element_1, Frame):

                        for frame_element_2 in frame_element_1.get_elements():
                            frame_element_2.render_button(surface)

    display_surface.blit(main_surface, (0, 0))
    pygame.display.update()

    clock.tick(max_FPS)

pygame.quit()
