import math

import arcade

import Consts


class Bee(arcade.Sprite):

    def __init__(self, image, scale):
        super().__init__(image, scale)
        self.speed = Consts.BEE_SPEED
        self.index = 0
        self.go_to_right = True

    def update(self):

        start_x = self.center_x

        if self.go_to_right is True:
            dest_x = self.center_x + 1
            self.index += 1
        else:
            dest_x = self.center_x - 1
            self.index -= 1

        if self.index > Consts.BEE_INTERVAL:
            self.go_to_right = False
        elif self.index < -Consts.BEE_INTERVAL:
            self.go_to_right = True

        x_diff = dest_x - start_x

        angle = math.atan2(0, x_diff)

        change_x = math.cos(angle) * self.speed

        self.center_x += change_x
