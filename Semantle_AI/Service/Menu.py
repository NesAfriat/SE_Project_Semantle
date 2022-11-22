# import Semantle_AI.Business.ModerFactory as MF
# import Semantle_AI.Business.ModelTrainer as WE
# from Play import Play
#
#
# class Menu:
#     model = None
#     vocabulary = None
#     trained = False
#     Exit_Menu = 0
#     trained_model_name = "word2vec.wordvectors"
#
#     def play_with_host_only(self):
#         off_on = input(
#             "\n==================================================\n1.Play offline.\n2.Play online.\n3.exit\n")
#         done = False
#         while not done:
#             if off_on == '1':
#                 if self.model is None:
#                     self.model, self.vocabulary,self.trained = MF.load_from_file(self.trained_model_name)
#                 play = Play(self.model, self.vocabulary)
#                 play.start_play_with_host_offline(self.trained)
#                 done = True
#             elif off_on == '2':
#                 print("Not possible yet...")
#             elif off_on == '3':
#                 done = True
#                 return
#             else:
#                 print("Illegal input, please try again.")
#
#     def train_again(self):
#         if len(self.model) == 0:
#             print("Model not exists")
#         self.model, self.vocabulary = WE.train_existing_model(model=self.model)
#
#     def admin_menu(self):
#         print("\n==================================================\nPlease choose and option:\n1.Create new model."
#               "\n2.load pre-trained model.\n4.retrain your model. \n3.Back to previous menu.")
#         is_good = False
#         while not is_good:
#             option = input()
#             if option == '1':
#                 self.model, self.vocabulary = WE.train_new_model()
#                 self.trained = True
#                 is_good = True
#             elif option == '2':
#                 self.model, self.vocabulary,self.trained = MF.load_from_file(self.trained,self.trained_model_name)
#                 is_good = True
#             elif option == '3':
#                 if not self.trained:
#                     print("model cannot be trained because it is downloaded as keyed vector format.\n in order to "
#                           "retrain model, you need to create it.")
#                     continue
#                 self.train_again()
#                 is_good = True
#             elif option == '3':
#                 is_good = True
#             else:
#                 option = input("Illegal input, please try again.")
#                 is_good = True
#
#     def check_option(self, value):
#         Exit_Menu = 0
#         while not Exit_Menu:
#             if value == '1':
#                 self.play_with_host_only()
#                 return
#             elif value == '2':
#                 self.admin_menu()
#                 return
#             elif value == '3':
#                 Exit_Menu = 1
#             else:
#                 print("Illegal input, please try again ")
#
#     def start_menu(self):
#         # switch cases here:
#         options = "1.Play semantle. \n2.Admin menu \n3.exit\nAnswer: "
#         options_num = 2
#         while self.Exit_Menu != '0':
#             value = input(
#                 f"\n\n\n\n\n==================================================\n Hello,  \nChoose an option from the menu:\n{options}")
#             try:
#                 while (not value.isnumeric()) and (value > (options_num + 1) or value == 0):
#                     value = input("Illegal option. please try again: \n")
#                 self.check_option(value)
#             except ValueError:
#                 print(ValueError)
