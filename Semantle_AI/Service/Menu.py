import Semantle_AI.Business.LoadModel as LM
import Semantle_AI.Business.ModelTrainer as WE
from Play import Play




class Menu:

    model = None
    vocabulary = None
    Exit_Menu = 0

    def play_with_host_only(self):
        off_on = input("\n==================================================\n1.Play offline.\n2.Play online.\n3.exit\n")
        done = False
        while not done:
            if off_on == '1':
                if self.model is None:
                    self.model, self.vocabulary = LM.load_from_file()
                play = Play(self.model, self.vocabulary)
                play.start_play_with_host_offline()
                done = True
            elif off_on == '2':
                print("Not possible yet...")
            elif off_on == '3':
                done = True
                return
            else:
                print("Illegal input, please try again.")

    def train_again(self):
        if len(self.model) == 0:
            print("Model not exists")
        model, vocabulary = WE.train_existing_model(model=self.model)

    def admin_menu(self):
        print("\n==================================================")
        option = input("Please choose and option:\n1.Create new model.\n2.load model from files. \n3.reTrain existing "
                       "model\n4.Back to previous menu.")
        isGood = False
        while not isGood:
            if option == '1':
                self.model, self.vocabulary = WE.train_new_model()
                isGood = True
            elif option == '2':
                self.model, self.vocabulary = LM.load_from_file()
                isGood = True
            elif option == '3':
                self.train_again()
                isGood = True
            elif option == '4':
                isGood = True
            else:
                option = input("Illegal input, please try again.")
                isGood = True

    def check_option(self,value):
        Exit_Menu = 0
        while not Exit_Menu:
            if value == '1':
                self.play_with_host_only()
                return
            elif value == '2':
                self.admin_menu()
                return
            elif value == '3':
                Exit_Menu = 1
            else:
                print("Illegal input, please try again ")

    def start_menu(self):
        # switch cases here:#
        options = "1.Play semantle. \n2.Admin menu \n3.exit\nAnswer: "
        options_num = 2
        while self.Exit_Menu != '0':
            value = input(
                f"\n\n\n\n\n==================================================\n Hello,  \nChoose an option from the menu:\n{options}")
            while (not value.isnumeric()) and (value > (options_num + 1) or value == 0):
                value = input("Illegal option. please try again: \n")
            self.check_option(value)
