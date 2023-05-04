from Game.GameBuilder import GameBuilder
import TransformInput



class Menu:
    def __init__(self):
        self.game_builder= GameBuilder()
        self.input_games=[]
        self.finish= False
        self.game_manager= None

    def validate_input(self,path):
        pass

    def transform_input(self,path):
        try:
            self.input_games += TransformInput.transform_input(path)
        except:
            print("Input transformation has failed- check configuration file")


    def build_game(self):
        self.validate_input("./configurations.json")
        self.transform_input("./configurations.json")
        self.game_manager=self.game_builder.build(self.input_games)
        print(len(self.input_games), "games added")


    def start_menu(self):
        while not self.finish:
            choice = input("\nChoose the desired action:\n1.Build game from file\n2.Run games\n3.Clear games\n4.Reports menu\n5.Leave\n")
            match choice:
                case '1':
                    self.build_game()
                case '2':
                    self.run_games()
                case '3':
                    self.clear_games()
                case '4':
                    self.reports_menu()
                case '5':
                    self.finish=True
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
        pass


