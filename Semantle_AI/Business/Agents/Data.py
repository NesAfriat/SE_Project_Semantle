from copy import copy
from collections import OrderedDict
from queue import PriorityQueue
import queue


class Data:
    def __init__(self):
        self.words_heap = PriorityQueue()
        self.guesses = dict()
        self.scores = dict()
        self.model = None
        self.remain_words = None
        self.last_score = -1
        self.last_word = None
        self.statistics = OrderedDict()
        self.copy_vocab = None
        self.error = 1

    def add_to_dict(self, word, distance):
        if word not in self.guesses.keys():
            self.last_score = distance
            self.last_word = word
            self.guesses[word] = (distance, self.model.get_word_vec(word))
            self.scores[word] = distance

    def set_model(self, model):
        self.model = model
        self.remain_words = copy(self.model.get_vocab())
        # initialize the max heap. All weights are 0.
        while not self.words_heap.empty():
            self.words_heap.get()
        for word in self.remain_words:
            self.words_heap.put(MyItem(word, 0))
        self.copy_vocab = copy(self.remain_words)

    def get_most_similar(self, vec):
        return self.model.get_most_similar_by_vec(vec)

    def get_word_vec(self, w):
        return self.model.get_word_vec(w)

    def get_guesses(self):
        return self.guesses
    def get_scores(self):
        return self.scores

    def get_distances(self):
        return [x for x, y in self.guesses.values()]

    def get_points(self):
        return [y for x, y in self.guesses.values()]

    def get_words(self):
        return self.guesses.keys()

    def execute_data(self):
        pass

    def set_error(self, error):
        self.error = error

    def reset(self):
        self.guesses = dict()
        self.statistics = OrderedDict()
        self.last_score = -1
        self.last_word = None

    def reset_vocab(self):
        self.remain_words = copy(self.copy_vocab)
        # init the max heap. All weights are 0.
        while not self.words_heap.empty():
            self.words_heap.get()
        for word in self.remain_words:
            self.words_heap.put(MyItem(word, 0))

    def get_statistics(self):
        return self.statistics

    def update_statistic(self):
        # Get last key
        if len(self.statistics) == 0:
            next_pos = 0
        else:
            next_pos = next(reversed(self.statistics)) + 1
        self.statistics[next_pos] = len(self.remain_words)

    def heap_top(self):
        # Get the largest element from the heap
        largest = self.words_heap.queue[0]
        return largest

    def heap_pop(self):
        # Pop the largest element from the heap
        largest = self.words_heap.get()
        return largest

    def heap_remove(self, word):
        # Remove the 'word' pair by key
        with self.words_heap.mutex:
            self.words_heap.queue = [
                item for item in self.words_heap.queue if item.word != word
            ]
            queue.heapify(self.words_heap.queue)

    def remove_by_word(self, word):
        # create a new priority queue
        new_pq = PriorityQueue()

        # remove the item with the matching word from the original priority queue
        while not self.words_heap.empty():
            item = self.words_heap.get()
            if item.word != word:
                new_pq.put(item)

        # replace the original priority queue with the new one
        self.words_heap = new_pq.queue
        self.words_heap.put = new_pq.put
        self.words_heap.get = new_pq.get


# class made for the heap compare function that doesn't know how to compare tuple.
class MyItem:
    def __init__(self, word: str, weight: int):
        self.word = word
        self.weight = weight

    def __lt__(self, other):
        return self.weight < other.weight

    def __repr__(self):
        return f'{self.word} ({self.weight})'

    def __eq__(self, other):
        if isinstance(other, MyItem):
            return self.word == other.word and self.weight == other.weight
        return False
