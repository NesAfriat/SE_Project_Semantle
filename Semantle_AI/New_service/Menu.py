import os

from Semantle_AI.Business.Game.GameBuilder import GameBuilder
from Semantle_AI.New_service import TransformInput


class Menu:
    def __init__(self):
        self.game_builder = GameBuilder()
        self.input_games = []
        self.finish = False
        self.game_manager = None

    def validate_input(self, path):
        pass

    def transform_input(self, path):
        try:
            self.input_games += TransformInput.transform_input(path)
        except Exception as e:
            print(f"Input transformation has failed- check configuration file\n error {e}")

    def build_games(self):
        if "Tests" in os.getcwd():
            path = replace_subdir(os.getcwd(), "Tests", "Semantle_AI")
            path = os.path.join(path, "New_Service", "configurations.json")
        else:
            path = os.path.join(os.getcwd(), "New_Service", "configurations.json")

        self.validate_input(path)
        self.transform_input(path)
        self.game_manager = self.game_builder.build(self.input_games)
        print(len(self.input_games), "games added")

    def start_menu(self):
        while not self.finish:
            choice = input("\nChoose the desired action:\n1.Build game from file\n2.Run games\n3.Clear "
                           "games\n4.Leave\n")
            match choice:
                case '1':
                    self.build_games()
                case '2':
                    self.run_games()
                case '3':
                    self.clear_games()
                case '4':
                    self.finish = True
                case _:
                    print("illegal input - please choose an option from 1-5")

    def run_games(self):
        if not self.game_manager:
            print("Please build some games to run first")
        else:
            self.game_manager.run_games()

    def clear_games(self):
        self.game_manager.clear_games()

    def reports_menu(self):
        pass  # import graph from path


def replace_subdir(path, old_subdir, new_subdir):
    path_parts = path.split(os.sep)
    updated_path_parts = [new_subdir if part == old_subdir else part for part in path_parts]
    updated_path = os.sep.join(updated_path_parts)
    return updated_path
