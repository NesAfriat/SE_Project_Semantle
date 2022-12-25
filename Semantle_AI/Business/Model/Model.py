

class Model:
    def __init__(self, model):
        self.model = model
        self.vocab = None

    def get_distance_of_word(self, word1, word2):
        ans = self.model.similarity(word1, word2)
        return ans

    def get_word_from_distance(self, dis: float) -> str:
        pass

    def get_most_similar(self, word):
        return self.model.most_similar(word)

    def get_vocab(self):
        if self.vocab is None:
            self.vocab = list(self.model.key_to_index)
            self.vocab = filter((lambda x: x.isalpha()), self.vocab)
            self.vocab = [x for x in self.vocab]
        return self.vocab
