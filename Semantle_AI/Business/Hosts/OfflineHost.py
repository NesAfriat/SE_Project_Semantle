from random import choice

from Business.Hosts.Host import Host


#  let similarity = getCosSim(guessVec, secretVec) * 100.0;
# function dot(f1, f2) {
#     return f1.reduce(function(sum, a, idx) {
#         return sum + a*f2[idx];
#     }, 0);
# }
#
# function getCosSim(f1, f2) {
#     return dot(f1,f2)/(mag(f1)*mag(f2));
# }
class OfflineHost(Host):

    def quitGame(self):
        pass

    def __init__(self):
        self.model = None
        self.vocabulary = None
        self.secret_word = None

    def get_model(self):
        return self.model

    def set_model(self, model):
        self.model = model
        self.vocabulary = set(self.model.get_vocab())

    def select_word_and_start_game(self):
        word = choice(list(self.vocabulary))
        self.secret_word = word

    def check_word(self, word):
        if word not in self.vocabulary:
            return -1
        else:
            return self.model.get_distance_of_word(word, self.secret_word)

    def set_word(self, new_word):
        self.secret_word = new_word

    def in_vocab(self, neww, trained):
        # keyed vector model type
        if trained:
            ans = neww in self.vocabulary
            return ans
        else:
            ans = neww in self.vocabulary
            return ans

    def most_similar(self):
        return self.model.get_most_similar(self.secret_word)
