class Data:
    def __init__(self):
        self.guesses = dict()
        self.last_guess = None
        self.last_dist = None

    def add_to_dict(self, word, distance):
        if word not in self.guesses:
            self.last_dist = distance
            self.last_guess = word
            self.guesses[word] = distance

    def get_guesses(self):
        return self.guesses

    def get_distances(self):
        return self.guesses.values()

    def get_words(self):
        return self.guesses.keys()

    def execute_data(self):
        pass

    def get_points(self):
        pass
