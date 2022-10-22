class World:
    def __init__(self, agent, environment):
        self.__environment = environment
        self.__agent = agent

        radars = self.__environment.radars
        self.agent.init_qtable(radars)

        self.reset(False)

    def reset(self, append_score=True):
        self.__agent.reset(self.__environment.start, append_score)

    def step(self, new_radar):
        action = self.agent.best_action()
        ##TODO l'environnement n'a rien a faire il fournit juste les fonction is_rock ...
        # reward, state = self.environment.do(self.agent.current_radar, action, self.__agent.current_radar, new_radar)


        # self.agent.step(reward, state, action, new_radar)
        # return action, reward

    ## c'est dégueu
    def make_learn(self, iterations):
        for i in range(iterations):
            self.reset()
            while not self.environment.is_treasure(self.agent.current_radar):
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
