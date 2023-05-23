# class made for the heap compare function that doesn't know how to compare tuple.
class MyItem:
    def __init__(self, word: str, weight: int):
        self.word = word
        self.error_vec = []
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight or (self.weight == other.weight and self.word < other.word)

    def __repr__(self):
        return f'{self.word} ({self.weight})'

    def __eq__(self, other):
        if isinstance(other, MyItem):
            return self.word == other.word and self.weight == other.weight
        return False

    def __hash__(self):
        return hash((self.word, self.weight))

