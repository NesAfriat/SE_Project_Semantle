from abc import ABC, abstractmethod


class Host(ABC):

    # check if the guess word is match
    @abstractmethod
    def check_word(self, word):
        pass

    # select word and start game
    @abstractmethod
    def select_word_and_start_game(self, out):
        pass

    # select word and start game
    @abstractmethod
    def start_game(self, out):
        pass

    # select word and start game
    @abstractmethod
    def quitGame(self):
        pass

    @abstractmethod
    def getWord(self):
        pass

    @abstractmethod
    def set_model_error(self, noise):
        pass

    @abstractmethod
    def getWordVec(self, word):
        pass

    @abstractmethod
    def setWord(self, word):
        pass
