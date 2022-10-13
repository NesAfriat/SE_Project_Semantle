class Model:
    def __init__(self,model):
        self.model=model

    def get_distance_of_word(self, word1,word2):
        return self.model.wv.similarity(word1, word2)

    def get_word_from_distance(self, dis: float) -> str:
        pass
