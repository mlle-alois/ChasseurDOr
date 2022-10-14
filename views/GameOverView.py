import arcade
import tkinter as tk

class GameOverView(arcade.View):
    def __init__(self, agent, width, height, is_won):
        super().__init__()
        self.__root = tk.Tk()
        self.__agent = agent
        self.__width = width
        self.__height = height
        self.__is_won = is_won

    def on_show_view(self):
        if self.__is_won:
            arcade.set_background_color(arcade.color.YELLOW)
        else:
            arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()

        if self.__is_won:
            arcade.draw_text("You won !", self.__width / 2, self.__height / 2,
                             arcade.color.BLACK, font_size=54, anchor_x="center")
            arcade.draw_text("Click to restart.", self.__width / 2, self.__height / 2 - 75,
                             arcade.color.GRAY, font_size=20, anchor_x="center")
        else:
            arcade.draw_text("You loose !", self.__width / 2, self.__height / 2,
                             arcade.color.WHITE, font_size=54, anchor_x="center")
            arcade.draw_text("Click to restart.", self.__width / 2, self.__height / 2 - 75,
                             arcade.color.GRAY, font_size=20, anchor_x="center")

        #TODO pouvoir activer cette ligne pour relancer le jeu automatiquement après X secondes

        # self.__root.after(3000, self.restart_game())


    def restart_game(self):
        from views.GameView import GameView
        game_view = GameView(self.__agent, self.__width, self.__height)
        game_view.setup()
        self.window.show_view(game_view)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        from views.GameView import GameView
        game_view = GameView(self.__agent, self.__width, self.__height)
        game_view.setup()
        self.window.show_view(game_view)



