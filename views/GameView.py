import arcade

import Consts
from bee import Bee


class GameView(arcade.View):
    def __init__(self, agent, width, height):
        super().__init__()

        self.__agent = agent
        self.__width = width
        self.__height = height

        self.__rock_sprites = arcade.SpriteList()
        self.__log_sprites = arcade.SpriteList()
        self.__iteration = 1
        self.__bee_list = None
        self.__heart_list = None

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.__walls = arcade.SpriteList()
        self.__bee_list = arcade.SpriteList()
        self.__heart_list = arcade.SpriteList()

        for state in self.__agent.environment.states:
            if self.__agent.environment.is_wall(state):
                sprite = arcade.Sprite(":resources:images/topdown_tanks/treeGreen_large.png", 0.5)

                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__walls.append(sprite)
            elif self.__agent.environment.is_rock(state):
                sprite = arcade.Sprite(":resources:images/tiles/rock.png", 0.25)

                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__rock_sprites.append(sprite)

            elif self.__agent.environment.is_log(state):
                sprite = arcade.Sprite(":resources:images/tiles/boxCrate_single.png", 0.25)

                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__log_sprites.append(sprite)

            elif self.__agent.environment.is_river(state):
                sprite = arcade.Sprite(":resources:images/tiles/water.png", 0.25)
                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__walls.append(sprite)
            elif self.__agent.environment.is_bee(state):
                sprite = Bee(":resources:images/enemies/bee.png",
                             0.25)
                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__bee_list.append(sprite)

        position_x = 200
        for pv in range(self.__agent.environment.pv):
            sprite = arcade.Sprite("pictures/heart.png", 0.05)
            sprite.center_x, sprite.center_y = position_x, 50
            self.__heart_list.append(sprite)
            position_x += 30

        self.__goal = arcade.Sprite("pictures/tresor.png", 0.07)
        self.__goal.center_x, self.__goal.center_y = self.state_to_xy(self.__agent.environment.treasure)

        self.__adventurer = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk3.png", 0.3)
        self.__adventurer.center_x, self.__adventurer.center_y = self.state_to_xy(self.__agent.state)

        self.__pickaxe = arcade.Sprite(
            "pictures/pickaxe.png", 0.05)
        self.__pickaxe.center_x, self.__pickaxe.center_y = self.state_to_xy_tool(self.__agent.state)

        self.__pickaxe_info = arcade.Sprite(
            "pictures/pickaxe.png", 0.08)
        self.__pickaxe_info.center_x, self.__pickaxe_info.center_y = 100, 50

        self.__sword = arcade.Sprite(
            ":resources:gui_basic_assets/items/sword_gold.png", 0.3)
        self.__sword.center_x, self.__sword.center_y = self.state_to_xy_tool(self.__agent.state)

        self.__sword_info = arcade.Sprite(
            ":resources:gui_basic_assets/items/sword_gold.png", 0.6)
        self.__sword_info.center_x, self.__sword_info.center_y = 100, 50

    def state_to_xy(self, state):
        return (state[1] + 0.5) * Consts.SPRITE_SIZE, \
               (self.__agent.environment.height - state[0] - 0.5) * Consts.SPRITE_SIZE

    def state_to_xy_tool(self, state):
        return (state[1] + 0.9) * Consts.SPRITE_SIZE, \
               (self.__agent.environment.height - state[0] - 0.7) * Consts.SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
        self.__rock_sprites.draw()
        self.__log_sprites.draw()
        self.__goal.draw()
        self.__adventurer.draw()
        self.__bee_list.draw()
        self.__heart_list.draw()

        if self.__agent.state[2] == Consts.PICKAXE:
            self.__tool = 'Pickaxe'
            self.__pickaxe.draw()
            self.__pickaxe_info.draw()
        else:
            self.__tool = 'Sword'
            self.__sword.draw()
            self.__sword_info.draw()

        arcade.draw_text("Press Esc. to pause",
                         self.__width / 2,
                         self.__height - 25,
                         arcade.color.WHITE,
                         font_size=20,
                         anchor_x="center")

        arcade.draw_text(
            f"Tool :      PV : {self.__agent.environment.pv}",
            10, 40, arcade.csscolor.WHITE, 20)
        arcade.draw_text(
            f"#{self.__iteration} Score : {self.__agent.score} T°C : {self.__agent.exploration}",
            10, 10, arcade.csscolor.WHITE, 20)

    def new_game(self):
        self.__agent.reset()
        self.setup()
        self.__iteration += 1

    def on_update(self, delta_time):
        from views.GameOverView import GameOverView
        if self.__agent.environment.is_dead():
            self.new_game()
            game_over_view = GameOverView(self, self.__agent, self.__width, self.__height, is_won=False, restart_automatically=Consts.RESTART_AUTOMATICALLY)
            self.window.show_view(game_over_view)
        elif self.__agent.environment.is_treasure(self.__agent.state):
            self.new_game()
            game_over_view = GameOverView(self, self.__agent, self.__width, self.__height, is_won=True, restart_automatically=Consts.RESTART_AUTOMATICALLY)
            self.window.show_view(game_over_view)
        else:
            action, reward = self.__agent.step()
            self.__adventurer.center_x, self.__adventurer.center_y = self.state_to_xy(self.__agent.state)
            self.__sword.center_x, self.__sword.center_y = self.state_to_xy_tool(self.__agent.state)
            self.__pickaxe.center_x, self.__pickaxe.center_y = self.state_to_xy_tool(self.__agent.state)
            self.__rock_sprites.update()
            self.__bee_list.update()
            self.__heart_list.update()

            hit_rock_list = arcade.check_for_collision_with_list(self.__adventurer, self.__rock_sprites)
            hit_bee_list = arcade.check_for_collision_with_list(self.__adventurer, self.__bee_list)

            for rock in hit_rock_list:
                rock.remove_from_sprite_lists()

            # TODO problème il y a 2 dans la hit list donc on enlève toujours 2 points de vie au lieu de 1
            #  + quand le personnage est déjà mort une fois il meurt super vite (en 1 coup ?)
            for bee in hit_bee_list:
                if self.__tool == 'Sword':
                    bee.remove_from_sprite_lists()
                else:
                    self.__agent.environment.lifePoints -= 1
                    if len(self.__heart_list) > 0:
                        self.__heart_list[len(self.__heart_list) - 1].remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.new_game()
        elif key == arcade.key.H:
            self.__agent.heat()
        elif key == arcade.key.ESCAPE:
            from views.PauseView import PauseView
            pause = PauseView(self, self.__width, self.__height)
            self.window.show_view(pause)