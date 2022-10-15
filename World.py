class World:
    def __init__(self, agent, environment):
        self.__environment = environment
        self.__agent = agent

        self.agent.init_qtable(self.environment.states)
        self.reset(False)

    def reset(self, append_score=True):
        self.__agent.reset(self.__environment.start, append_score)

    def step(self):
        action = self.agent.best_action()
        reward, state = self.environment.do(self.agent.state, action)

        self.agent.step(reward, state, action)
        #return action, reward

    def make_learn(self, iterations):
        for i in range(iterations):
            self.reset()
            while not self.environment.is_treasure(self.agent.state):
                self.step()
        self.reset()

    @property
    def environment(self):
        return self.__environment

    @property
    def agent(self):
        return self.__agent
