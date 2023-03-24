from Game.AgentBuilder import AgentBuilder
from Game.GameManager import GameManager
from Game.HostBuilder import HostBuilder


class GameBuilder():
    def __init__(self):
        self.agent_builder= AgentBuilder()
        self.host_builder= HostBuilder()


    def build_agent_host(self,game):
        self.host_builder.create_host(game["host"])
        self.host_builder.with_model(game["host_model"])
        host = self.host_builder.get_host()
        self.agent_builder.create_agent(game["agent"])
        self.agent_builder.with_id(game["id"])
        self.agent_builder.with_algo(game["algorithm"])
        self.agent_builder.with_model(game["agent_model"])
        self.agent_builder.with_host(host)
        return self.agent_builder.get_agent()

    def build(self,games):
        game_manager = GameManager()
        for game in games:
            agent = self.build_agent_host(game)
            game_manager.add_game(agent, game["runs"])
        return game_manager

