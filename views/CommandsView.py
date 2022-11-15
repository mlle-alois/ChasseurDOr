import arcade


class CommandsView(arcade.View):
    def __init__(self, game_view, width, height):
        super().__init__()
        self.__game_view = game_view
        self.__width = width
        self.__height = height

    def on_show_view(self):
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        self.clear()

        arcade.draw_text("Commands", self.__width / 2, self.__height - 50,
                         arcade.color.BLACK, font_size=30, anchor_x="center")

        arcade.draw_text("MOVE -> Arrows",
                         self.__width / 2,
                         self.__height - 100,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")

        arcade.draw_text("PULL -> Z, Q, S, D",
                         self.__width / 2,
                         self.__height - 130,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")

        arcade.draw_text("SWITCH TOOL -> S",
                         self.__width / 2,
                         self.__height - 160,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")

        arcade.draw_text("CHANGE GAME MODE -> P",
                         self.__width / 2,
                         self.__height - 190,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")

        arcade.draw_text("EXPLORATION -> H",
                         self.__width / 2,
                         self.__height - 220,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")

        arcade.draw_text("RESTART -> R",
                         self.__width / 2,
                         self.__height - 250,
                         arcade.color.BLACK,
                         font_size=15,
                         anchor_x="center")

        arcade.draw_text("Press Esc. to return",
                         self.__width / 2,
                         self.__height - 290,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            self.window.show_view(self.__game_view)
