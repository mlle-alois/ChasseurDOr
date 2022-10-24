import arcade

import Consts
from Bee import Bee
from views.GameOverView import GameOverView
from views.PauseView import PauseView


class GameView(arcade.View):
    def __init__(self, world, width, height):
        super().__init__()

        self.__world = world
        self.__width = width
        self.__height = height

        self.__walls = arcade.SpriteList()
        self.__rock_sprites = arcade.SpriteList()
        self.__log_sprites = arcade.SpriteList()
        self.__bee_list = arcade.SpriteList()
        self.__heart_list = arcade.SpriteList()
        self.__all_the_sprites = arcade.SpriteList()

        self.__goal = None
        self.__adventurer = None
        self.__pickaxe = None
        self.__pickaxe_info = None
        self.__sword = None
        self.__sword_info = None

        self.__iteration = 1

        self.__tool = Consts.PICKAXE

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        ##garder les coordonnées dans env
        agent_state = self.__world.agent.state

        for points in self.__world.environment.map_coordinates:
            if self.__world.environment.is_wall(points):
                sprite = self.__create_sprite(
                    ":resources:images/topdown_tanks/treeGreen_large.png",
                    0.5,
                    points,
                    Consts.MAP_WALL
                )

                self.__walls.append(sprite)
                self.__all_the_sprites.append(sprite)

            elif self.__world.environment.is_rock(points):
                sprite = self.__create_sprite(
                    ":resources:images/tiles/rock.png",
                    0.25,
                    points,
                    Consts.ROCK
                )

                self.__rock_sprites.append(sprite)
                self.__all_the_sprites.append(sprite)

            elif self.__world.environment.is_log(points):
                sprite = self.__create_sprite(
                    ":resources:images/tiles/boxCrate_single.png",
                    0.25,
                    points,
                    Consts.LOG
                )

                self.__log_sprites.append(sprite)
                self.__all_the_sprites.append(sprite)

            elif self.__world.environment.is_river(points):
                sprite = self.__create_sprite(
                    ":resources:images/tiles/water.png",
                    0.25,
                    points,
                    Consts.RIVER
                )

                self.__walls.append(sprite)
                self.__all_the_sprites.append(sprite)

            elif self.__world.environment.is_bee(points):
                sprite = Bee(":resources:images/enemies/bee.png", 0.25)
                sprite.center_x, sprite.center_y = self.state_to_xy(points)
                sprite.properties['name'] = Consts.BEE

                self.__bee_list.append(sprite)
                self.__all_the_sprites.append(sprite)

        position_x = 200
        for pv in range(self.__world.agent.life_points):
            sprite = self.__create_sprite(
                "pictures/heart.png",
                0.05,
                (position_x, 50)
            )
            self.__heart_list.append(sprite)
            position_x += 30

        self.__goal = arcade.Sprite("pictures/tresor.png", 0.07)
        self.__goal.center_x, self.__goal.center_y = self.state_to_xy(self.__world.environment.treasure)
        self.__goal.properties['name'] = Consts.TREASURE
        self.__all_the_sprites.append(self.__goal)

        self.__adventurer = self.__create_sprite(
            ":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk3.png",
            0.3,
            agent_state
        )

        self.__pickaxe = self.__create_tool_sprite("pictures/pickaxe.png", 0.05, agent_state)

        self.__pickaxe_info = arcade.Sprite("pictures/pickaxe.png", 0.08)
        self.__pickaxe_info.center_x, self.__pickaxe_info.center_y = 100, 50

        self.__sword = self.__create_tool_sprite(":resources:gui_basic_assets/items/sword_gold.png", 0.3, agent_state)

        self.__sword_info = arcade.Sprite(":resources:gui_basic_assets/items/sword_gold.png", 0.6)
        self.__sword_info.center_x, self.__sword_info.center_y = 100, 50

    def state_to_xy(self, state):
        return (state[1] + 0.5) * Consts.SPRITE_SIZE, \
               (self.__world.environment.height - state[0] - 0.5) * Consts.SPRITE_SIZE

    def state_to_xy_tool(self, state):
        return (state[1] + 0.9) * Consts.SPRITE_SIZE, \
               (self.__world.environment.height - state[0] - 0.7) * Consts.SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
        self.__rock_sprites.draw()
        self.__log_sprites.draw()
        self.__goal.draw()
        self.__adventurer.draw()
        self.__bee_list.draw()
        self.__heart_list.draw()

        if self.__world.agent.state[2] == Consts.PICKAXE:
            self.__tool = Consts.PICKAXE
            self.__pickaxe.draw()
            self.__pickaxe_info.draw()
        else:
            self.__tool = Consts.SWORD
            self.__sword.draw()
            self.__sword_info.draw()

        arcade.draw_text(
            "Press Esc. to pause",
            self.__width / 2,
            self.__height - 25,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

        arcade.draw_text(
            f"Tool :      PV : {self.__world.agent.life_points}",
            10, 40, arcade.csscolor.WHITE, 20
        )
        arcade.draw_text(
            f"#{self.__iteration} Score : {self.__world.agent.score} T°C : {self.__world.agent.exploration}",
            10, 10, arcade.csscolor.WHITE, 20
        )

    def new_game(self):
        self.__world.reset()
        self.setup()
        ## Horrible trouver une autre manière de la faire
        self.__world.update_agent_radar(self.__get_radar())
        self.__iteration += 1

    def on_update(self, delta_time):
        agent_state = self.__world.agent.state

        if self.__world.agent.is_dead():
            self.new_game()
            game_over_view = GameOverView(
                self, self.__width, self.__height, is_won=False,
                restart_automatically=Consts.RESTART_AUTOMATICALLY
            )
            self.window.show_view(game_over_view)

        elif self.__world.agent_has_won():
            self.new_game()
            game_over_view = GameOverView(
                self, self.__width, self.__height, is_won=True,
                restart_automatically=Consts.RESTART_AUTOMATICALLY
            )
            self.window.show_view(game_over_view)

        else:
            agent_move = self.__world.step()

            self.__adventurer.center_x, self.__adventurer.center_y = self.state_to_xy(agent_move)
            self.__sword.center_x, self.__sword.center_y = self.state_to_xy_tool(agent_state)
            self.__pickaxe.center_x, self.__pickaxe.center_y = self.state_to_xy_tool(agent_state)

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
                if self.__tool == Consts.SWORD:
                    bee.remove_from_sprite_lists()
                else:
                    self.__world.agent.hurt()
                    if len(self.__heart_list) > 0:
                        self.__heart_list[len(self.__heart_list) - 1].remove_from_sprite_lists()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.new_game()
        elif key == arcade.key.H:
            self.__world.agent.heat()
        elif key == arcade.key.ESCAPE:
            pause = PauseView(self, self.__width, self.__height)
            self.window.show_view(pause)

    def __get_radar(self):
        radar = []

        for x in range(-30, 31, 30):
            for y in range(30, -31, -30):
                points = arcade.get_sprites_at_point(
                    (self.__adventurer.center_x + x, self.__adventurer.center_y + y),
                    self.__all_the_sprites
                )
                radar.append("" if len(points) == 0 else points[0].properties['name'])

        return radar

    def __create_sprite(self, picture_path, size, coordinate, token_name=""):
        sprite = arcade.Sprite(picture_path, size)
        sprite.center_x, sprite.center_y = self.state_to_xy(coordinate)
        sprite.properties['name'] = token_name

        return sprite

    def __create_tool_sprite(self, picture_path, size, coordinate):
        sprite = arcade.Sprite(picture_path, size)
        sprite.center_x, sprite.center_y = self.state_to_xy_tool(coordinate)

        return sprite
