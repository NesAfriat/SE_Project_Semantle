from Semantle_AI.Business.Game.ModelFactory import ModelFactory
from Semantle_AI.Business.Game.AgentBuilder import AgentBuilder
from Semantle_AI.Business.Game.GameManager import GameManager
from Semantle_AI.Business.Game.HostBuilder import HostBuilder





class GameBuilder():
    def __init__(self):
        self.agent_builder= AgentBuilder()
        self.host_builder= HostBuilder()
        self.model_factory= ModelFactory()
        self.id_counter= 0


    def build_agent_host(self,game):
        self.host_builder.create_host(game["host"])
        self.host_builder.with_model(game["host_model"])
        self.host_builder.with_distance_function(game["distance_function"])
        host = self.host_builder.get_host()
        self.agent_builder.create_agent_and_model(game["agent"],host, game["agent_model"], ModelFactory)
        self.agent_builder.with_id(self.id_counter)
        self.agent_builder.with_algo(game["algorithm"])
        return self.agent_builder.get_agent()

    def build(self,games):
        game_manager = GameManager()
        for game in games:
            agent = self.build_agent_host(game)
            game_manager.add_game(game["runs"], agent, game["game_type"])
            self.id_counter+=1
        return game_manager

