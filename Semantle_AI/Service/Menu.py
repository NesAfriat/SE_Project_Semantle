import os.path
from pathlib import Path

import Business.ModelFactory as MF
from Business.GameManager import GameManager
from Service.AgentMenu.Agent1Builder import Agent1Builder
from Service.AgentMenu.ManualAgentBuilder import ManualAgentBuilder


class Menu:
    pca = None

    def __init__(self):
        self.concrete_agent_builder = None
        self.finished = False
        self.out = lambda *args: print(*args)

    def start_menu(self):
        done_loop = False
        while not self.finished and not done_loop:
            choose = self.busy_choose("Choose agent", "Agent1", "Agent2", "Manual")
            if choose == '1':
                self.concrete_agent_builder = Agent1Builder(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.loop_times()
                done_loop = True
            elif choose == '2':
                self.concrete_agent_builder = Agent1Builder(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.loop_times()
                done_loop = True
            elif choose == '3':
                self.concrete_agent_builder = ManualAgentBuilder(self.out, input, self.finished)
                self.concrete_agent_builder.start_menu()
                self.loop_times()
                done_loop = True
            elif choose == 'e':
                done_loop = True

    def loop_times(self):
        self.concrete_agent_builder.get_result().start_play(self.out)

    def choose_agent(self):
        def choose_agent_model():
            ip = self.busy_choose(
                "Choose Agent Model", "Word2Vec")
            if ip == 'b':
                self.choose_agent()
            elif ip == '1':
                self.game_manager.create_agent1()
                self.game_manager.create_agent_word2vec_model_online()
                self.choose_algo()
            elif ip == 'e':
                self.finished = True

        ip = self.busy_choose("Choose Agent", "agent1", "agent2")
        if ip == 'b':
            self.human_or_AI_game()
        elif ip == '1':
            if self.offline_playing:
                self.game_manager.create_agent1()
                self.game_manager.set_agent_host_model()
                self.choose_algo()
            else:
                choose_agent_model()
        elif ip == '2':
            self.game_manager.create_agent1()
            choose_agent_model()
        elif ip == 'e':
            self.finished = True

    def busy_choose(self, to_write, *args):
        acc = ""
        num = 1
        for option in args:
            acc = acc + str(num) + ". " + option + "\n"
            num += 1
        num -= 1
        while True:
            ip = input("===================" + to_write + "===================\n\n" + acc)
            if ip == 'e' or ip == 'b' or (ip.isnumeric() and 0 < int(ip) <= num):
                return ip
            else:
                print("\nplease choose valid option please")

    def click_ok_and_start(self):
        ip = input("\npress enter to start...  \n")
        self.concrete_agent_builder.get_result().start()

    def start_commandline_game(self):
        self.game_manager.start_human_game(input, lambda m: print(m))
