from copy import copy
from collections import OrderedDict

import numpy as np
from Semantle_AI.Business.Container.MyItem import MyItem
from Semantle_AI.Business.Container.SortedList import SortedList
from Semantle_AI.Business.Container.State import State
from Semantle_AI.Business.Container.GuessScore import GuessScore


class Data:
    def __init__(self):
        # stores all words with their weights. for the choosing methods.
        self.words_heap = SortedList()
        # holds all guessed words with the distances.
        self.guesses = dict()
        # holds all distanced from the init words. that aren't calculated withing the play game
        # method. and needed to be checked separately.
        self.scores = []
        self.model = None
        self.remain_words = None
        self.last_score = -1
        self.last_word = None
        # holds game statistics by order for saving in the graphs and csv.
        self.statistics = OrderedDict()
        self.copy_vocab = None
        self.is_priority = False
        self.state = State()
        # caches dicts for the normal factor and entropy.
        self.normCache = OrderedDict()
        self.entropyCache = OrderedDict()

    def add_to_dict(self, word, distance):
        if word not in self.guesses.keys():
            self.last_score = distance
            self.last_word = word
            self.guesses[word] = (distance, self.model.get_word_vec(word))
            self.scores.append(GuessScore(word, distance))

    def update_state_map(self, word, score):
        self.state.update(word, score)
        for item in self.words_heap:
            new_weight, new_sum = self.ews(item.word, self.state)
            self.state.words_new_sum[item.word] = new_sum
            item.weight = new_weight
        self.state.words_new_sum[word] = self.ews(word, self.state)[1]

    def ews(self, w, s: State):
        if not s:
            raise ValueError("State (s) cannot be an empty list")
        # getting the new value in the state
        last_elem = s.lis[-1]
        word = last_elem[0]
        distance = last_elem[1]

        # calculating its distance
        dist = self.get_distance_of_word(w, word)
        # add it to the sum
        add_on = (dist - distance) ** 2
        if w in s.words_new_sum.keys():
            old_sum = s.words_new_sum[w]
        else:
            old_sum = 0
        return ((1 / len(s.lis)) * np.sqrt(old_sum + add_on)), old_sum + add_on

    def setError(self, err):
        self.model.setError(err)

    def set_Priority(self, value):
        self.is_priority = value

    def set_model(self, model):
        self.model = model
        self.remain_words = copy(self.model.get_vocab())
        # initialize the max heap. All weights are 0.
        self.words_heap = SortedList([MyItem(word, 0) for word in self.remain_words])
        self.copy_vocab = copy(self.remain_words)

    def set_model_and_vocab(self, model):
        self.model = model
        self.remain_words = copy(self.model.get_vocab())
        # initialize the max heap. All weights are 0.
        self.words_heap = SortedList([MyItem(word, 0) for word in self.remain_words])
        self.copy_vocab = copy(self.remain_words)
        self.normCache = OrderedDict()
        self.entropyCache = OrderedDict()

    def add_state_norm(self, state, norm):
        key = f"{len(state.lis)}_{state.lis[-1][0] if state.lis else ''}"  # creates a string key like '3_word'
        self.normCache[key] = norm  # Add the state to the dictionary
        self.update_state_norm()  # Check and remove states that don't meet the criteria

    def add_state_entropy(self, state, entropy):
        key = f"{len(state.lis)}_{state.lis[-1][0] if state.lis else ''}"  # creates a string key like '3_word'
        self.entropyCache[key] = entropy  # Add the state to the dictionary
        self.update_state_entropy()  # Check and remove states that don't meet the criteria

    def update_state_norm(self):
        current_length = None
        # Process keys
        for key in list(self.normCache.keys()):
            length, _ = key.split('_')  # Split the key into length and last word
            length = int(length)  # Convert length to integer
            if current_length is None:
                current_length = length
            if length < current_length - 2 or length > current_length:
                del self.normCache[key]  # Remove this state
            else:
                return

    def update_state_entropy(self):
        current_length = None
        # Process keys
        for key in list(self.entropyCache.keys()):
            length, _ = key.split('_')  # Split the key into length and last word
            length = int(length)  # Convert length to integer
            if current_length is None:
                current_length = length
            if length < current_length - 2 or length > current_length:
                del self.entropyCache[key]  # Remove this state
            else:
                return

    def get_state_norm(self, state):
        key = f"{len(state.lis)}_{state.lis[-1][0] if state.lis else ''}"  # creates a string key like '3_word'
        if key in self.normCache:
            return self.normCache.get(key)
        else:
            return -1

    def get_state_entropy(self, state):
        key = f"{len(state.lis)}_{state.lis[-1][0] if state.lis else ''}"  # creates a string key like '3_word'
        if key in self.entropyCache:
            return self.entropyCache.get(key)
        else:
            return -1

    def get_most_similar(self, vec):
        return self.model.get_most_similar_by_vec(vec)

    def get_word_vec(self, w):
        return self.model.get_word_vec(w)

    def get_guesses(self):
        return self.guesses

    def get_distances(self):
        return [x for x, y in self.guesses.values()]

    def get_distance_of_word(self, last_guess_word, word):

        return self.model.get_distance_of_word(last_guess_word, word)

    def get_points(self):
        return [y for x, y in self.guesses.values()]

    def get_words(self):
        return self.guesses.keys()

    def execute_data(self):
        pass

    def reset(self):
        self.guesses = dict()
        self.scores = []
        self.statistics = OrderedDict()
        self.last_score = -1
        self.last_word = None
        self.state.reset()
        self.normCache = OrderedDict()
        self.entropyCache = OrderedDict()

    def reset_vocab(self):
        self.remain_words = copy(self.copy_vocab)

        # init the max heap. All weights are 0.
        self.words_heap = SortedList([MyItem(word, 0) for word in self.remain_words])

    def get_statistics(self):
        return self.statistics

    def update_statistic(self):
        # Get last key
        if len(self.statistics) == 0:
            next_pos = 0
        else:
            next_pos = next(reversed(self.statistics)) + 1
        if self.is_priority:
            self.statistics[next_pos] = len(self.words_heap)
        else:
            self.statistics[next_pos] = len(self.remain_words)

