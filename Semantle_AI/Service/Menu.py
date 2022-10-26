from Business.GameHost import GameHost
from Service.Play import Play
import Business.ModelTrainer as WE
import Business.LoadModel as LM
from Play import Play

model = []
vocabulary = []
Exit_Menu = 0


def play_with_host_only():
    off_on = input("To play with the offline version press 1, To play online press 2. \n")
    if off_on == '1':
        play = Play()
        play.start_play_with_host_offline()
    elif off_on == '2':
        print("Not possible yet...")


def check_option(value):
    if value == '1':
        play_with_host_only()
    elif value == '2':
        Exit_Menu = 1

        # elif value == '2':
        #     WE.train_new_model(model)
        # elif value == '3':
        #     filename = input("\nPlease enter file name, or keep empty for default name.\n")
        #     LM.load_from_file(filename, model, vocabulary)
        # elif value == '4':
        #     filename = input("\nPlease enter file name, or keep empty for default name.\n")
        #     WE.train_new_model(model, filename)
        # elif value == '5':
        #     print("Option not possible yet....")


class Menu:

    def start_menu(self):
        # switch cases here:#
        options = "1.Play semantle. \n2.exit"
        options_num = 2
        while Exit_Menu != '0':
            value = input(
                f"\n\n\n\n\n==================================================\n Hello,  \nChoose an option from the menu:\n{options}\n")
            while (not value.isnumeric()) and (value > (options_num + 1) or value == 0):
                value = input("Illegal option. please try again: \n")
            check_option(value)
