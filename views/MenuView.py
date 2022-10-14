import arcade

from views.GameView import GameView


class MenuView(arcade.View):
    def __init__(self, agent, width, height):
        super().__init__()
        self.__agent = agent
        self.__width = width
        self.__height = height

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Gold Digger", self.__width / 2, self.__height / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to start.", self.__width / 2, self.__height / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game = GameView(self.__agent, self.__width, self.__height)
        game.setup()
        self.window.show_view(game)
