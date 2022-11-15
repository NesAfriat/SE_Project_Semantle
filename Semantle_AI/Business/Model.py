class Model:
    def __init__(self,model):
        self.model = model

    def get_distance_of_word(self, word1, word2):
        ans = self.model.similarity(word1, word2)
        return ans

    def get_word_from_distance(self, dis: float) -> str:
        pass

    def get_most_similar(self, word):
        return self.model.most_similar(word)
