import pygame


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
            self.colour = [32, 178, 170]
        if 'surface' in kwargs:
            self.surface = kwargs['surface']
        else:
            self.surface = 'display_surface'
