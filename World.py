class World:
    def __init__(self, agent, environment):
        self.__environment = environment
        self.__agent = agent
        self.reset(False)

    def reset(self, append_score=True):
        self.__agent.reset(self.__environment.start, append_score)

    def step(self, new_radar):
        action = self.agent.best_action()
        # tool = self.agent.tool
        agent_position = self.__agent.current_position()
        # reward, state, new_tool = self.environment.do(self.agent.current_radar, action, self.__agent.current_radar, tool, new_radar)

    #     move = Consts.ACTION_MOVES[action]
    #     tool = move[2] if move[2] != 0 else state[2]
    #     new_state = (state[0] + move[0], state[1] + move[1], tool)
    #     agent_position = new_state[5]
    #     reward = Consts.REWARD_DEFAULT
    #
    #     if self.is_forbidden_state(agent_position):
    #         reward = -2 * self.__nb_states
    #     elif self.is_obstacle(agent_position):
    #         if self.is_good_tool(agent_position, tool):
    #             state = new_state
    #         else:
    #             reward = -2
    #     elif self.is_bee(agent_position):
    #         state = new_state
    #         if not self.is_good_tool(agent_position, tool):
    #             reward = -3 * self.__nb_states
    #     else:
    #         state = new_state
    #         if self.is_treasure(agent_position):
    #             reward = 3 * self.__nb_states

    # self.agent.step(reward, state, action, new_radar)
    # return action, reward

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
        return self.__environment.is_treasure(self.__agent.current_radar[5])

    def update_agent_radar(self, new_radar):
        self.__agent.update_radar(new_radar)
