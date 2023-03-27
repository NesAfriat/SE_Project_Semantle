from Game.DataCollector import DataCollector


class GameManager():
    def __init__(self):
        self.games = []
        self.data_collector = DataCollector()

    def add_game(self, agent, runs_number):
        self.games.append((agent, runs_number))

    def run_games(self):
        for game in self.games:
            try:
                for i in range(game[1]):
                    self.data_collector.add_results(game[0].start_play())
            except:
                print("game number", i, "has failed")
