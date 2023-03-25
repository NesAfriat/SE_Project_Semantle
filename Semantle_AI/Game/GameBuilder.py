from Game.AgentBuilder import AgentBuilder
from Game.GameManager import GameManager
from Game.HostBuilder import HostBuilder


class GameBuilder():
    def __init__(self):
        self.agent_builder= AgentBuilder()
        self.host_builder= HostBuilder()
        self.id_counter= 0


    def build_agent_host(self,game):
        self.host_builder.create_host(game["host"])
        self.host_builder.with_model(game["host_model"])
        self.host_builder.with_distance_function(game["distance_function"])
        host = self.host_builder.get_host()
        self.agent_builder.create_agent_and_model(game["agent"],host,game["model"])
        self.agent_builder.with_id(self.id_counter)
        self.agent_builder.with_algo(game["algorithm"])
        return self.agent_builder.get_agent()

    def build(self,games):
        game_manager = GameManager()
        for game in games:
            agent = self.build_agent_host(game)
            game_manager.add_game(agent, game["runs"])
            self.id_counter+=1
        return game_manager

