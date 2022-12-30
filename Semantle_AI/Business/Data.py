class Data:
    def __init__(self):
        self.guesses = dict()
        self.last_guess = None
        self.last_dist = None

    def add_to_dict(self, word, distance, point):
        if word not in self.guesses:
            self.last_dist = distance
            self.last_guess = word
            self.guesses[word] = (distance, point)

    def get_guesses(self):
        return self.guesses

    def get_distances(self):
        return [x for x, y in self.guesses.values()]

    def get_points(self):
        return [y for x, y in self.guesses.values()]

    def get_words(self):
        return self.guesses.keys()

    def execute_data(self):
        pass
