class State:
    def __init__(self):
        self.lis = list()
        self.words_new_sum = dict()

    def reset(self):
        self.lis = list()
        self.words_new_sum = dict()

    def update(self, word, dist):
        self.lis.append((word, dist))

    def __eq__(self, other):
        if isinstance(other, State):
            return self.lis == other.lis and self.words_new_sum == other.words_new_sum
        return False

    def __hash__(self):
        return hash(tuple(self.lis))
