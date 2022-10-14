import arcade


class PauseView(arcade.View):
    def __init__(self, game_view, width, height):
        super().__init__()
        self.__game_view = game_view
        self.__width = width
        self.__height = height

    def on_show_view(self):
        arcade.set_background_color(arcade.color.ORANGE)

    def on_draw(self):
        self.clear()

        arcade.draw_text("PAUSED", self.__width / 2, self.__height / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")

        arcade.draw_text("Press Esc. to return",
                         self.__width / 2,
                         self.__height / 2 - 50,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.__game_view)
