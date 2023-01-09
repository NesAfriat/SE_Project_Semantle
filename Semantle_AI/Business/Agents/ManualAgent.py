from Business.Agents.Agent import Agent
from copy import copy


class ManualAgent(Agent):

    def guess_word(self, inp,  *args):
        word = input("-Enter your next word or 0 to return:\n")

    # def start_play(self, inp,  out):
    #     self.host.select_word_and_start_game(out)
    #     out("Try to Guess a word!")
    #     score = -1
    #     quit = False
    #     self.data.last_score = -2
    #     self.data.update_statistic()
    #     while abs(self.data.last_score) != 1.0 and abs(self.data.last_score) != 0 and not quit:
    #         word = self.guess_word(inp)
    #         spl = str.split(word, "$")
    #         if spl[0] == '@':
    #             self.host.setWord(spl[1])
    #         elif word != '0':
    #             score = self.host.check_word(word)
    #             if score == -2:
    #                 out("Word is not in the vocabulary, Please try another one.\n")
    #             else:
    #                 self.data.last_score = self.host.check_word(word)
    #                 self.last_word = word
    #                 self.update_statistic()
    #                 out(f"Guessed word is: {str(word)}.\t Similarity is: {str(round(score * 100, 2))} \n")
    #         else:
    #             quit = True
    #     if not quit:
    #         out("you won!!")
    #     else:
    #         out("see you next time!!")
    #     self.host.quitGame()


