from Business.Algorithms.Algorithm import Algorithm
import queue
from Business.Agents.Data import Data, MyItem


class SmartMultiLateration(Algorithm):
    def __init__(self, dist_formula):
        super().__init__()
        self.dist_formula = dist_formula

    def calculate(self):
        last_vec = self.data.get_word_vec(self.data.last_word)
        # Get the items from the priority queue
        items = []
        while not self.data.words_heap.empty():
            item = self.data.words_heap.get()
            items.append(item)

        # Modify the items
        for i, item in enumerate(items):
            dist = abs(self.dist_formula(self.data.get_word_vec(item.word), last_vec))
            distance_res = dist - self.data.last_score
            if round(distance_res, 10) <= 0:  # self.data.error:
                items[i] = MyItem(item.word, item.weight)
            else:
                items[i] = MyItem(item.word, (item.weight - (round((dist / self.data.last_score), 2))))

        # Push the modified items back into the priority queue
        for item in items:
            self.data.words_heap.put(item)

        # return the queue top.

        next_word = self.data.words_heap.get()
        if self.data.words_heap.empty():
            raise ValueError("error occurred, there are no words left to guess.")
        return next_word.word
