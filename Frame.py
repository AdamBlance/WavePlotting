from GUIElement import *


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
                    edge_of_last_object = element.top
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
                    edge_of_last_object = element.bottom
                else:
                    element.center = (self.centerx, middle_of_last_object + self.spacing)
                    middle_of_last_object = element.centery

    def get_elements(self):
        return self.elements
