import pygame


class Surface(pygame.Surface):
    all_surfaces = []

    def __init__(self, elements, size):

        super(Surface, self).__init__(size)

        self.elements = elements

        self.all_surfaces.append(self)

    def get_elements(self):
        return self.elements
