from GUIElement import *

pygame.init()


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

    def render_button(self, surface):

        if self.collidepoint(pygame.mouse.get_pos()) and not pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(surface, modify_colour(self.colour, 40), self)
            pygame.draw.rect(surface, self.colour, self.inflate(-8, -8))

        elif self.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            pygame.draw.rect(surface, modify_colour(self.colour, 40), self)
            pygame.draw.rect(surface, modify_colour(self.colour, -30), self.inflate(-8, -8))

        else:
            pygame.draw.rect(surface, modify_colour(self.colour, -30), self)
            pygame.draw.rect(surface, self.colour, self.inflate(-8, -8))

        button_centre = (self.centerx - self.text.get_rect().centerx, self.centery - self.text.get_rect().centery)
        surface.blit(self.text, button_centre)
