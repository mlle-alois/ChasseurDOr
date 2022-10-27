import Consts


class World:
    def __init__(self, agent, environment):
        self.__environment = environment
        self.__agent = agent
        self.reset(False)

    def reset(self, append_score=True):
        self.__agent.reset(self.__environment.start, append_score)

    def step(self):
        env = self.__environment
        action = self.agent.best_action()
        tool = self.agent.tool

        reward = Consts.REWARD_DEFAULT
        agent_move = Consts.ACTION_MOVES[action]
        self.agent.update_position(action)

        if self.agent.is_on_forbidden_state():
            agent_move = (0, 0)
            reward = -2 * env.map_size
            print("forbidden state")
        elif self.agent.is_on_obstacle():
            if self.agent.has_good_tool():
                agent_move = (0, 0)
                reward = -2
        elif self.agent.is_on_bee():
            if not self.agent.has_good_tool():
                reward = -3 * env.map_size
        else:
            if self.agent.is_on_treasure():
                reward = 3 * env.map_size

        return agent_move, reward, action

    ## c'est dégueu #oui
    def make_learn(self, iterations):
        for i in range(iterations):
            self.reset()
            # while not self.agent_has_won():
            #     ## TODO
            #     # self.step()
        self.reset()

    @property
    def environment(self):
        return self.__environment

    @property
    def agent(self):
        return self.__agent

    def agent_has_won(self):
        return self.agent.is_on_treasure()

    def update_agent_radar(self, new_radar):
        self.__agent.update_radar(new_radar)
