import arcade

from views.GameView import GameView


class MenuView(arcade.View):
    def __init__(self, world, width, height):
        super().__init__()
        self.__world = world
        self.__width = width
        self.__height = height

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        self.clear()
        self.__adventurer = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk3.png", 1.5)
        self.__adventurer.center_x, self.__adventurer.center_y = 120, self.__height / 2
        self.__adventurer.draw()

        self.__treasure = arcade.Sprite("pictures/tresor.png", 0.25)
        self.__treasure.center_x, self.__treasure.center_y = 680, self.__height / 2
        self.__treasure.draw()

        arcade.draw_text("Gold Digger", self.__width / 2, self.__height / 2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to start.", self.__width / 2, self.__height / 2 - 75,
                         arcade.color.GRAY, font_size=20, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game = GameView(self.__world, self.__width, self.__height)
        game.setup()
        self.window.show_view(game)
