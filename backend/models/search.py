import os
import unicodedata
import numpy as np
import fasttext
import fasttext.util
from konlpy.tag import Okt


script_dir = os.path.dirname(os.path.abspath(__file__))
base_path = os.path.join(script_dir, "..", "static", "tag")

TARGET_WORDS = os.listdir(base_path)


class FastText():
    def __init__(self):
        fasttext.util.download_model("ko", if_exists="ignore")
        self.fasttext = fasttext.load_model("cc.ko.300.bin")
        self.targets = np.array(TARGET_WORDS)
        targets_vector = np.stack([self.fasttext.get_word_vector(word) for word in self.targets], axis=0)
        self.targets_vector = targets_vector / np.linalg.norm(targets_vector, ord=2, axis=1, keepdims=True)

    def get_similar_words(self, words, topk=12):
        words_vector = np.stack([self.fasttext.get_word_vector(word) for word in words], axis=0)
        words_vector = words_vector / np.linalg.norm(words_vector, ord=2, axis=1, keepdims=True)
        similarity = np.dot(self.targets_vector, words_vector.T)

        top_similatity = np.max(similarity, axis=1)
        topk_similar_words = self.targets[np.argsort(top_similatity)[::-1][:topk]].tolist()
        return topk_similar_words


def stemmer(text):
    okt = Okt()  
    words = okt.nouns(text)  
    return words


def get_mapped_words(words):
    mapped_words = []
    for word in words:
        if word in TARGET_WORDS:
            mapped_words.append(word)
        if word in ["사람", "배", "트럭", "차"]:
            mapped_words.append(f"{word} (1)")
            mapped_words.append(f"{word} (2)")
    return mapped_words