import os
import numpy as np
import fasttext
from konlpy.tag import Okt


TARGET_WORDS = list(map(lambda x: x.rstrip(".png"), os.listdir("../data/drawings")))


class FastText():
    def __init__(self):
        fasttext.utils.download_model("ko", if_exists="ignore")
        self.fasttext = fasttext.load_model("cc.ko.300.bin")
        self.targets = np.array(TARGET_WORDS)
        targets_vector = np.stack([self.fasttext.get_word_vector(word) for word in self.sketch_words], axis=0)
        self.targets_vector = targets_vector / np.linalg.norm(targets_vector, ord=2, axis=1, keepdims=True)

    def get_similar_words(self, words, topk=10):
        words_vector = np.stack([self.fasttext.get_word_vector(word) for word in words], axis=0)
        words_vector = words_vector / np.linalg.norm(words_vector, ord=2, axis=1, keepdims=True)
        similarity = np.dot(self.targets_vector, words_vector.T)

        top_similatity = np.max(similarity, axis=1)
        topk_similat_words = self.targets[np.argsort(top_similatity)[::-1][:topk]].tolist()
        return topk_similat_words


def stemmer(text):
    okt = Okt()  
    words = okt.nouns(text)  
    return words


def get_mapped_words(words):
    mapped_words = []
    for word in words:
        if word in TARGET_WORDS:
            mapped_words.append(word)
    return mapped_words