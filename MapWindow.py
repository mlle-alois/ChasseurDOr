import arcade

import Consts


class MapWindow(arcade.Window):
    def __init__(self, agent):
        super().__init__(agent.environment.width * Consts.SPRITE_SIZE,
                         agent.environment.height * Consts.SPRITE_SIZE,
                         'Gold Digger')

        self.__obstacles_sprites = arcade.SpriteList()
        self.__agent = agent
        self.__iteration = 1

    def setup(self):
        self.__walls = arcade.SpriteList()

        for state in self.__agent.environment.states:
            if self.__agent.environment.is_wall(state):
                sprite = arcade.Sprite(":resources:images/topdown_tanks/treeGreen_large.png", 0.5)

                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__walls.append(sprite)
            elif self.__agent.environment.is_rock(state):
                sprite = arcade.Sprite(":resources:images/tiles/stone.png", 0.25)

                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                # self.__walls.append(sprite)
                self.__obstacles_sprites.append(sprite)

            elif self.__agent.environment.is_log(state):
                sprite = arcade.Sprite(":resources:images/topdown_tanks/treeBrown_large.png", 0.5)

                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__obstacles_sprites.append(sprite)
            elif self.__agent.environment.is_river(state):
                sprite = arcade.Sprite(":resources:images/tiles/water.png", 0.25)
                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__walls.append(sprite)
            elif self.__agent.environment.is_bee(state):
                sprite = arcade.Sprite(":resources:images/enemies/bee.png", 0.25)
                sprite.center_x, sprite.center_y = self.state_to_xy(state)
                self.__walls.append(sprite)

        self.__goal = arcade.Sprite(":resources:images/items/coinGold.png", 0.5)
        self.__goal.center_x, self.__goal.center_y = self.state_to_xy(self.__agent.environment.treasure)

        self.__adventurer = arcade.Sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk3.png", 0.3)
        self.__adventurer.center_x, self.__adventurer.center_y = self.state_to_xy(self.__agent.state)

    def state_to_xy(self, state):
        return (state[1] + 0.5) * Consts.SPRITE_SIZE, \
               (self.__agent.environment.height - state[0] - 0.5) * Consts.SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
        self.__obstacles_sprites.draw()
        self.__goal.draw()
        self.__adventurer.draw()

        if self.__agent.state[2] == Consts.AXE:
            tool = 'Axe'
        elif self.__agent.state[2] == Consts.PICKAXE:
            tool = 'Pickaxe'
        else:
            tool = 'Sword'

        arcade.draw_text(
            f"#{self.__iteration} Score : {self.__agent.score} T°C : {self.__agent.exploration} Tool : {tool} PV : {self.__agent.environment.pv}",
            10, 10, arcade.csscolor.WHITE, 20)

    def new_game(self):
        self.setup()
        self.__agent.reset()
        self.__iteration += 1

    def on_update(self, delta_time):
        if self.__agent.environment.is_dead(self.__agent.state) or \
                self.__agent.environment.is_treasure(self.__agent.state):
            self.new_game()
        else:
            action, reward = self.__agent.step()
            self.__adventurer.center_x, self.__adventurer.center_y = self.state_to_xy(self.__agent.state)
            # Call update on all sprites (The sprites don't do much in this
            # example though.)
            self.__obstacles_sprites.update()

            # Generate a list of all sprites that collided with the player.
            hit_list = arcade.check_for_collision_with_list(self.__adventurer, self.__obstacles_sprites)

            # Loop through each colliding sprite, remove it, and add to the score.
            for rock in hit_list:
                rock.remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.new_game()
        elif key == arcade.key.H:
            self.__agent.heat()
