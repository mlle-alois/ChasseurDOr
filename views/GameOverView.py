import threading

import arcade

from Bee import Bee


class GameOverView(arcade.View):
    def __init__(self, game_view, width, height, is_won, restart_automatically):
        super().__init__()
        self.__game_view = game_view
        self.__width = width
        self.__height = height
        self.__is_won = is_won
        self.__restart_automatically = restart_automatically

        self.__treasure = None
        self.__bee = None

    def on_show_view(self):
        if self.__is_won:
            arcade.set_background_color(arcade.color.YELLOW)
        else:
            arcade.set_background_color(arcade.color.BLACK)

        if self.__restart_automatically:
            start_time = threading.Timer(1, self.restart_game)
            start_time.start()

    def on_draw(self):
        self.clear()

        if self.__is_won:
            self.__treasure = arcade.Sprite("pictures/tresor.png", 0.25)
            self.__treasure.center_x, self.__treasure.center_y = 680, self.__height / 2
            self.__treasure.draw()

            arcade.draw_text("You won !", self.__width / 2, self.__height / 2,
                             arcade.color.BLACK, font_size=54, anchor_x="center")
            arcade.draw_text("Click to restart.", self.__width / 2, self.__height / 2 - 75,
                             arcade.color.GRAY, font_size=20, anchor_x="center")
        else:
            arcade.draw_text("You loose !", self.__width / 2, self.__height / 2,
                             arcade.color.WHITE, font_size=54, anchor_x="center")
            arcade.draw_text("Click to restart.", self.__width / 2, self.__height / 2 - 75,
                             arcade.color.GRAY, font_size=20, anchor_x="center")

            self.__bee = Bee(":resources:images/enemies/bee.png",
                             1)
            self.__bee.center_x, self.__bee.center_y = 680, self.__height / 2
            self.__bee.draw()

    def restart_game(self):
        self.window.show_view(self.__game_view)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        self.window.show_view(self.__game_view)
