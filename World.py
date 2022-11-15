import Consts


class World:
    def __init__(self, agent, environment):
        self.__environment = environment
        self.__agent = agent
        self.reset(False)

    def reset(self, treasure_radar, append_score=True):
        self.__agent.reset(self.__environment.start, treasure_radar, append_score)

    def step(self, action):
        env = self.__environment
        if action is None:
            action = self.agent.best_action()

        reward = Consts.REWARD_DEFAULT
        agent_move = Consts.ACTION_MOVES[action]

        ## char comme #, $ ...
        new_position = self.agent.current_radar[Consts.RADAR_ACTION_INDEX[action]]

        if self.agent.is_on_forbidden_state(new_position):
            agent_move = (0, 0)
            reward = -2 * env.map_size
        elif self.agent.is_on_rock(new_position) and not self.agent.has_good_tool(new_position):
            agent_move = (0, 0)
            reward = -2
        elif self.agent.is_on_log(new_position) and not self.agent.can_interact_with_log(action):
            agent_move = (0, 0)
            reward = -2
        elif self.agent.is_on_bee(new_position) and not self.agent.has_good_tool(new_position):
            reward = -3 * env.map_size
        else:
            if self.agent.is_on_treasure(new_position):
                reward = 3 * env.map_size

        return agent_move, reward, action

    @property
    def environment(self):
        return self.__environment

    @property
    def agent(self):
        return self.__agent

    def agent_has_won(self, radar):
        return radar[Consts.AGENT_POSITION_IN_RADAR] == Consts.TREASURE

    def update_agent_radar(self, new_radar, treasure_radar):
        self.__agent.update_radars(new_radar, treasure_radar)
