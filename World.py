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
        # reward, state, new_tool = self.environment.do(self.agent.current_radar, action, tool, new_radar)

        agent_move = Consts.ACTION_MOVES[action]
        # reward = Consts.REWARD_DEFAULT
        #
        # if env.is_forbidden_state(agent_position):
        #     reward = -2 * env.map_size
        # elif env.is_obstacle(agent_position):
        #     if env.is_good_tool(agent_position, tool):
        #         state = new_state
        #     else:
        #         reward = -2
        # elif env.is_bee(agent_position):
        #     state = new_state
        #     if not env.is_good_tool(agent_position, tool):
        #         reward = -3 * env.map_size
        # else:
        #     state = new_state
        #     if env.is_treasure(agent_position):
        #         reward = 3 * env.map_size
        #
        # self.agent.step(reward, state, action, new_radar)

        return agent_move

    ## c'est dégueu #oui
    def make_learn(self, iterations):
        for i in range(iterations):
            self.reset()
            while not self.agent_has_won():
                print("qsmoldihzldjsghaerfjzmkzdfhjgjhsfmdkenjg")
                ## TODO
                # self.step()
        self.reset()

    @property
    def environment(self):
        return self.__environment

    @property
    def agent(self):
        return self.__agent

    def agent_has_won(self):
        return self.__environment.is_agent_on_treasure(self.__agent.current_radar[5])

    def update_agent_radar(self, new_radar):
        self.__agent.update_radar(new_radar)
