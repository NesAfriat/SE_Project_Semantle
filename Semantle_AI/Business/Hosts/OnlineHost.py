from abc import ABC

from Semantle_AI.Business.Hosts.Host import Host


class OnlineHost(Host):

    ## check if the guess word is match
    def check_word(self, word):
        return 1

    ## select word and start game
    def select_word_and_start_game(self):
        print("need start game here")