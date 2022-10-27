import time

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

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
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
                sprite.center_x, sprite.center_y = self.coordinates_to_xy(points)
                sprite.properties['name'] = Consts.BEE

                self.__bee_list.append(sprite)
                self.__all_the_sprites.append(sprite)
            elif self.__world.environment.is_start(points):
                self.__adventurer = self.__create_sprite(
                    ":resources:images/animated_characters/female_adventurer/femaleAdventurer_walk3.png",
                    0.3,
                    points,
                    Consts.AGENT
                )
                self.__pickaxe = self.__create_tool_sprite("pictures/pickaxe.png", 0.05, points)
                self.__sword = self.__create_tool_sprite(":resources:gui_basic_assets/items/sword_gold.png", 0.3,
                                                         points)

        position_x = 200

        # TODO voir pour garder, ça risque de gêner le radar
        for pv in range(self.__world.agent.life_points):
            sprite = self.__create_sprite(
                "pictures/heart.png",
                0.05,
                (position_x, 50),
                ""
            )
            self.__heart_list.append(sprite)
            position_x += 30

        self.__goal = arcade.Sprite("pictures/tresor.png", 0.07)
        self.__goal.center_x, self.__goal.center_y = self.coordinates_to_xy(self.__world.environment.treasure)
        self.__goal.properties['name'] = Consts.TREASURE
        self.__all_the_sprites.append(self.__goal)

        self.__pickaxe_info = arcade.Sprite("pictures/pickaxe.png", 0.08)
        self.__pickaxe_info.center_x, self.__pickaxe_info.center_y = 100, 50

        self.__sword_info = arcade.Sprite(":resources:gui_basic_assets/items/sword_gold.png", 0.6)
        self.__sword_info.center_x, self.__sword_info.center_y = 100, 50

    def coordinates_to_xy(self, coordinates):
        return (coordinates[1] + 0.5) * Consts.SPRITE_SIZE, \
               (self.__world.environment.height - coordinates[0] - 0.5) * Consts.SPRITE_SIZE

    def coordinates_to_xy_tool(self, coordinates):
        return (coordinates[1] + 0.9) * Consts.SPRITE_SIZE, \
               (self.__world.environment.height - coordinates[0] - 0.7) * Consts.SPRITE_SIZE

    def on_draw(self):
        arcade.start_render()
        self.__walls.draw()
        self.__rock_sprites.draw()
        self.__log_sprites.draw()
        self.__goal.draw()
        self.__adventurer.draw()
        self.__bee_list.draw()
        self.__heart_list.draw()

        if self.__world.agent.tool == Consts.PICKAXE:
            self.__pickaxe.draw()
            self.__pickaxe_info.draw()
        else:
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
        ## TODO Horrible trouver une autre manière de la faire
        self.__world.update_agent_radar(self.__get_radar())
        self.__iteration += 1

    def on_update(self, delta_time):
        radar = self.__get_radar()

        self.__world.update_agent_radar(radar)
        self.__world.agent.add_radar_to_qtable(radar)

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
            agent_move, reward, action = self.__world.step()
            self.__world.agent.step(reward, radar, action)

            self.__adventurer.center_x, self.__adventurer.center_y = self.__adventurer.center_x + agent_move[0], \
                                                                     self.__adventurer.center_y + agent_move[1]
            # self.__adventurer.center_x, self.__adventurer.center_y = self.coordinates_to_xy(agent_move)

            ##TODO après agent
            self.__sword.center_x, self.__sword.center_y = self.coordinates_to_xy_tool(agent_move)
            self.__pickaxe.center_x, self.__pickaxe.center_y = self.coordinates_to_xy_tool(agent_move)

            self.__rock_sprites.update()
            self.__bee_list.update()
            self.__heart_list.update()

            hit_rock_list = arcade.check_for_collision_with_list(self.__adventurer, self.__rock_sprites)
            hit_bee_list = arcade.check_for_collision_with_list(self.__adventurer, self.__bee_list)

            for rock in hit_rock_list:
                rock.remove_from_sprite_lists()

            for bee in hit_bee_list:
                if self.__world.agent.tool == Consts.SWORD:
                    bee.remove_from_sprite_lists()
                else:
                    self.__world.agent.hurt()
                    if len(self.__heart_list) > 0:
                        self.__heart_list[len(self.__heart_list) - 1].remove_from_sprite_lists()

            print("action")
            print(action)
            print("agent_move")
            print(agent_move)
            time.sleep(2)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.R:
            self.new_game()
        elif key == arcade.key.H:
            self.__world.agent.heat()
        elif key == arcade.key.ESCAPE:
            pause = PauseView(self, self.__width, self.__height)
            self.window.show_view(pause)

    ## TODO Radar en flocon
    def __get_radar(self):
        radar = []

        # for w in range(0, 3):
        #     if w == 0 or w == 2:
        #         start_index = 30
        #         end_index = 31
        #     else:
        #         start_index = 60
        #         end_index = 61
        #
        #     for x in range(-start_index, end_index, 30):
        #         for y in range(start_index, -end_index, -30):
        #             points = arcade.get_sprites_at_point(
        #                 (self.__adventurer.center_x + x, self.__adventurer.center_y + y),
        #                 self.__all_the_sprites
        #             )
        #             radar.append("" if len(points) == 0 else points[0].properties['name'])
        for x in range(-30, 31, 30):
            for y in range(30, -31, -30):
                points = arcade.get_sprites_at_point(
                    (self.__adventurer.center_x + x, self.__adventurer.center_y + y),
                    self.__all_the_sprites
                )
                radar.append("" if len(points) == 0 else points[0].properties['name'])

        return radar

    def __create_sprite(self, picture_path, size, coordinate, token_name):
        sprite = arcade.Sprite(picture_path, size)
        sprite.center_x, sprite.center_y = self.coordinates_to_xy(coordinate)
        sprite.properties['name'] = token_name

        return sprite

    def __create_tool_sprite(self, picture_path, size, coordinate):
        sprite = arcade.Sprite(picture_path, size)
        sprite.center_x, sprite.center_y = self.coordinates_to_xy_tool(coordinate)

        return sprite
