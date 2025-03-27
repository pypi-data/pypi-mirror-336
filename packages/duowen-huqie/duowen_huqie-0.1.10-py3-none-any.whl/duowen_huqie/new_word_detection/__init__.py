import logging
from copy import deepcopy
from typing import List

from duowen_huqie.nlp import NLP
from .model import TrieNode
from ..nlp.re_pattern import PATTERN_NEWLINE, PATTERN_SPACE_TAB, PATTERN_PUNCTUATION_AND_SPECIAL_CHARS
from ..nlp.stopwords import STOPWORDS
from ..utils import record_time


class NewWordDetection:
    def __init__(self, nlp: NLP):
        self.nlp = nlp
        self.word_freq = self.load_dictionary()
        self.ori_root = TrieNode('*', self.word_freq)

    def load_dictionary(self) -> dict:
        """
        加载外部词频记录
        :param filename:
        :return:
        """
        word_freq = {}
        with open(self.nlp.tokenizer.DIR_ + '.txt', 'r') as f:
            for line in f:
                try:
                    line_list = line.split(' ')
                    word_freq[line_list[0]] = line_list[1]
                except IndexError as e:
                    continue
        fnm = self.nlp.tokenizer.DIR_ + '.txt'
        try:

            of = open(fnm, 'r', encoding="utf-8")
            while True:
                line = of.readline()
                if not line:
                    break
                line = PATTERN_NEWLINE.sub("", line)
                line = PATTERN_SPACE_TAB.split(line)
                word_freq[line[0]] = line[1]
            of.close()
        except Exception:
            logging.exception(f"[NewWordDetection]:Build word_freq {fnm} failed")

        for k, v in self.nlp.new_word.items():
            word_freq[k] = line_list[v["frequency"]]

        return word_freq

    @staticmethod
    def split_text(text) -> List[str]:

        sentences = PATTERN_PUNCTUATION_AND_SPECIAL_CHARS.split(text)
        return [s.strip() for s in sentences if s.strip()]

    @staticmethod
    def generate_ngram(input_list, n):
        result = []
        for i in range(1, n + 1):
            result.extend(zip(*[input_list[j:] for j in range(i)]))
        return result

    def split_sentences_word(self, text: str) -> List[List[str]]:
        _data = []
        for i in self.split_text(text):
            _data.append([j for j in self.nlp.content_sm_cut(i).split() if j not in STOPWORDS])
        return _data

    @staticmethod
    def dynamic_threshold(N, base_threshold=5, ref_length=10000, alpha=0.5):
        return int(max(2, base_threshold * (ref_length / N) ** alpha))

    @record_time()
    def find_word(self, text: str, ngram=3, top_n=None):
        _root = deepcopy(self.ori_root)
        _N = 0

        for word_list in self.split_sentences_word(text):
            _N += len(''.join(word_list))
            ngrams = self.generate_ngram(word_list, ngram)
            for d in ngrams:
                _root.add(d)
        return _root.find_word(top_n or self.dynamic_threshold(_N))
