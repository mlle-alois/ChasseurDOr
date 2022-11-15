import arcade

import Consts
from Bee import Bee
from views.GameOverView import GameOverView
from views.PauseView import PauseView
from views.CommandsView import CommandsView
from utils.RadarUtils import *


class GameView(arcade.View):
    def __init__(self, world, width, height, play_mode: bool):
        super().__init__()

        self.__world = world
        self.__width = width
        self.__height = height
        self.__play_mode = play_mode

        self.__walls = arcade.SpriteList()
        self.__heart_list = arcade.SpriteList()
        self.__all_the_sprites = None
        self.__bee_list = None
        self.__rock_sprites = None
        self.__log_sprites = None

        self.__treasure = None
        self.__adventurer = None
        self.__pickaxe = None
        self.__pickaxe_info = None
        self.__sword = None
        self.__sword_info = None

        self.__iteration = 1

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.__bee_list = arcade.SpriteList()
        self.__rock_sprites = arcade.SpriteList()
        self.__log_sprites = arcade.SpriteList()
        self.__all_the_sprites = arcade.SpriteList()

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

        for pv in range(self.__world.agent.life_points):
            sprite = arcade.Sprite("pictures/heart.png", 0.05)
            sprite.center_x, sprite.center_y = (position_x, 50)

            self.__heart_list.append(sprite)
            position_x += 30

        self.__treasure = arcade.Sprite("pictures/tresor.png", 0.07)
        self.__treasure.center_x, self.__treasure.center_y = self.coordinates_to_xy(self.__world.environment.treasure)
        self.__treasure.properties['name'] = Consts.TREASURE
        self.__all_the_sprites.append(self.__treasure)

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
        self.__treasure.draw()
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
            "Press Esc. to pause / C to see commands",
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
        self.__world.reset(self.__get_treasure_radar())
        self.setup()
        self.__world.update_agent_radar(self.__get_radar(), self.__get_treasure_radar())
        self.__iteration += 1

    def on_update(self, delta_time):
        radar = self.__get_radar()

        self.__world.update_agent_radar(radar, self.__get_treasure_radar())
        self.__world.agent.add_radar_to_qtable(radar)

        if self.__world.agent.is_dead():
            self.new_game()
            game_over_view = GameOverView(
                self, self.__width, self.__height, is_won=False,
                restart_automatically=Consts.RESTART_AUTOMATICALLY
            )
            self.window.show_view(game_over_view)

        elif self.__world.agent_has_won(radar):
            self.new_game()
            game_over_view = GameOverView(
                self, self.__width, self.__height, is_won=True,
                restart_automatically=Consts.RESTART_AUTOMATICALLY
            )
            self.window.show_view(game_over_view)

        else:
            if not self.__play_mode:
                self.__step(None, radar)

    def __step(self, action, radar):
        agent_move, reward, action = self.__world.step(action)

        self.__world.agent.step(reward, radar, self.__get_treasure_radar(), action)

        self.move_log(action, agent_move)

        self.__adventurer.center_x, self.__adventurer.center_y = self.__adventurer.center_x + agent_move[0], \
                                                                 self.__adventurer.center_y + agent_move[1]

        self.__move_tool_sprite(agent_move)

        self.__rock_sprites.update()
        self.__bee_list.update()
        self.__heart_list.update()

        self.__remove_rock_sprite()
        self.__remove_bee_sprite()

    def move_log(self, action, agent_move):
        points = []
        # On cherche à récupérer le sprite qu'on bouge -> Le log
        # Ici on bouge la caisse en dessous de nous, soit pour la tirer vers le haut, soit pour la pousser vers le bas
        if action == Consts.ACTION_PULL_UP or action == Consts.ACTION_DOWN:
            points = arcade.get_sprites_at_point(
                (self.__adventurer.center_x, self.__adventurer.center_y - Consts.SPRITE_SIZE),
                self.__log_sprites
            )
        elif action == Consts.ACTION_PULL_DOWN or action == Consts.ACTION_UP:
            points = arcade.get_sprites_at_point(
                (self.__adventurer.center_x, self.__adventurer.center_y + Consts.SPRITE_SIZE),
                self.__log_sprites
            )
        elif action == Consts.ACTION_PULL_RIGHT or action == Consts.ACTION_LEFT:
            points = arcade.get_sprites_at_point(
                (self.__adventurer.center_x - Consts.SPRITE_SIZE, self.__adventurer.center_y),
                self.__log_sprites
            )
        elif action == Consts.ACTION_PULL_LEFT or action == Consts.ACTION_RIGHT:
            points = arcade.get_sprites_at_point(
                (self.__adventurer.center_x + Consts.SPRITE_SIZE, self.__adventurer.center_y),
                self.__log_sprites
            )

        if len(points) > 0:
            points[0].center_x, points[0].center_y = points[0].center_x + agent_move[0], points[0].center_y + \
                                                     agent_move[1]

    # Supprime les sprites rocher sur lesquel l'aventurier est
    def __remove_rock_sprite(self):
        hit_rock_list = arcade.check_for_collision_with_list(self.__adventurer, self.__rock_sprites)

        for rock in hit_rock_list:
            rock.remove_from_sprite_lists()

    # Supprime les sprites abeilles que l'aventurier a tué
    def __remove_bee_sprite(self):
        hit_bee_list = arcade.check_for_collision_with_list(self.__adventurer, self.__bee_list)

        for bee in hit_bee_list:
            if self.__world.agent.tool == Consts.SWORD:
                bee.remove_from_sprite_lists()
                continue
            self.__world.agent.hurt()
            if len(self.__heart_list) > 0:
                self.__heart_list[len(self.__heart_list) - 1].remove_from_sprite_lists()

    def __move_tool_sprite(self, agent_move):
        self.__sword.center_x, self.__sword.center_y = self.__sword.center_x + agent_move[0], \
                                                       self.__sword.center_y + agent_move[1]
        self.__pickaxe.center_x, self.__pickaxe.center_y = self.__pickaxe.center_x + agent_move[0], \
                                                       self.__pickaxe.center_y + agent_move[1]

    def on_key_press(self, key, modifiers):
        radar = self.__get_radar()
        if key == arcade.key.R:
            self.new_game()
        elif key == arcade.key.H:
            self.__world.agent.heat()
        elif key == arcade.key.ESCAPE:
            pause = PauseView(self, self.__width, self.__height)
            self.window.show_view(pause)
        elif key == arcade.key.C:
            pause = CommandsView(self, self.__width, self.__height)
            self.window.show_view(pause)

        # Change le mode de jeu (test ou jouable)
        elif key == arcade.key.P:
            self.__play_mode = not self.__play_mode

        # MODE JEU
        elif key == arcade.key.UP:
            self.__step(Consts.ACTION_UP, radar)
        elif key == arcade.key.DOWN:
            self.__step(Consts.ACTION_DOWN, radar)
        elif key == arcade.key.RIGHT:
            self.__step(Consts.ACTION_RIGHT, radar)
        elif key == arcade.key.LEFT:
            self.__step(Consts.ACTION_LEFT, radar)
        elif key == arcade.key.Z:
            self.__step(Consts.ACTION_PULL_UP, radar)
        elif key == arcade.key.S:
            self.__step(Consts.ACTION_PULL_DOWN, radar)
        elif key == arcade.key.D:
            self.__step(Consts.ACTION_PULL_RIGHT, radar)
        elif key == arcade.key.Q:
            self.__step(Consts.ACTION_PULL_LEFT, radar)
        elif key == arcade.key.T:
            action = Consts.ACTION_PICKAXE
            if self.__world.agent.tool == Consts.PICKAXE:
                action = Consts.ACTION_SWORD
            self.__step(action, radar)

    # Radar en flocon
    def __get_radar(self):
        radar = []

        for x in range(-30, 31, 30):
            for y in range(30, -31, -30):
                points = arcade.get_sprites_at_point(
                    (self.__adventurer.center_x + x, self.__adventurer.center_y + y),
                    self.__all_the_sprites
                )
                radar.append(" " if len(points) == 0 else points[0].properties['name'])

        ## Point en haut du radar: index 9
        points = arcade.get_sprites_at_point(
            (self.__adventurer.center_x + 0, self.__adventurer.center_y + 60),
            self.__all_the_sprites
        )
        radar.append(" " if len(points) == 0 else points[0].properties['name'])

        ## Point à droite du radar: index 10
        points = arcade.get_sprites_at_point(
            (self.__adventurer.center_x + 60, self.__adventurer.center_y + 0),
            self.__all_the_sprites
        )
        radar.append(" " if len(points) == 0 else points[0].properties['name'])

        ## Point en bas du radar: index 11
        points = arcade.get_sprites_at_point(
            (self.__adventurer.center_x + 0, self.__adventurer.center_y - 60),
            self.__all_the_sprites
        )
        radar.append(" " if len(points) == 0 else points[0].properties['name'])

        ## Point à gauche du radar: index 12
        points = arcade.get_sprites_at_point(
            (self.__adventurer.center_x - 60, self.__adventurer.center_y + 0),
            self.__all_the_sprites
        )
        radar.append(" " if len(points) == 0 else points[0].properties['name'])

        return radar

    def __get_treasure_radar(self):
        treasure_radar = []

        for x in range(-30, 31, 30):
            for y in range(30, -31, -30):
                treasure_radar.append("")

        if is_treasure_above_agent(self.__adventurer, self.__treasure):
            treasure_radar[3] = Consts.TREASURE_INDICATOR
        elif is_treasure_under_agent(self.__adventurer, self.__treasure):
            treasure_radar[5] = Consts.TREASURE_INDICATOR
        elif is_treasure_left_to_agent(self.__adventurer, self.__treasure):
            treasure_radar[1] = Consts.TREASURE_INDICATOR
        elif is_treasure_right_to_agent(self.__adventurer, self.__treasure):
            treasure_radar[7] = Consts.TREASURE_INDICATOR
        elif is_treasure_diagonal_up_left_to_agent(self.__adventurer, self.__treasure):
            treasure_radar[0] = Consts.TREASURE_INDICATOR
        elif is_treasure_diagonal_up_right_to_agent(self.__adventurer, self.__treasure):
            treasure_radar[6] = Consts.TREASURE_INDICATOR
        elif is_treasure_diagonal_down_left_to_agent(self.__adventurer, self.__treasure):
            treasure_radar[2] = Consts.TREASURE_INDICATOR
        elif is_treasure_diagonal_down_right_to_agent(self.__adventurer, self.__treasure):
            treasure_radar[8] = Consts.TREASURE_INDICATOR

        return treasure_radar

    def __create_sprite(self, picture_path, size, coordinate, token_name):
        sprite = arcade.Sprite(picture_path, size)
        sprite.center_x, sprite.center_y = self.coordinates_to_xy(coordinate)
        sprite.properties['name'] = token_name

        return sprite

    def __create_tool_sprite(self, picture_path, size, coordinate):
        sprite = arcade.Sprite(picture_path, size)
        sprite.center_x, sprite.center_y = self.coordinates_to_xy_tool(coordinate)

        return sprite
