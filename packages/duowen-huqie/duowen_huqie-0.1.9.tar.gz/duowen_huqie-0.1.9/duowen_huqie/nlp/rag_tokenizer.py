import copy
import logging
import math
import os
import string

import datrie
import nltk
from nltk import word_tokenize
from nltk.data import find
from nltk.stem import PorterStemmer, WordNetLemmatizer

from duowen_huqie.utils import tradi2simp, strQ2B
from .re_pattern import (PATTERN_ENDS_WITH_LETTER, PATTERN_LOWERCASE_DOT_HYPHEN, PATTERN_NUMERIC_COMMA_DOT_HYPHEN,
                         PATTERN_NEWLINE, PATTERN_SPACE_TAB, PATTERN_SPACE, PATTERN_SPLIT_CHARS, PATTERN_NON_WORD_CHARS,
                         PATTERN_NUMERIC_PERIOD_HYPHEN, PATTERN_ALPHA_UNDERSCORE_HYPHEN)


def ensure_nltk_resource(resource_name):
    try:
        find(resource_name)
    except LookupError:
        logging.info(f"Resource '{resource_name}' not found. Downloading...")
        nltk.download(resource_name.split("/")[-1])


ensure_nltk_resource("tokenizers/punkt_tab")
ensure_nltk_resource("corpora/wordnet")

_curr_dir = os.path.dirname(os.path.abspath(__file__))


class RagTokenizer:
    def key_(self, line):
        return str(line.lower().encode("utf-8"))[2:-1]

    def rkey_(self, line):
        return str(("DD" + (line[::-1].lower())).encode("utf-8"))[2:-1]

    def loadDict_(self, fnm):
        logging.info(f"[HUQIE]:Build trie from {fnm}")
        try:
            of = open(fnm, "r", encoding="utf-8")
            while True:
                line = of.readline()
                if not line:
                    break
                line = PATTERN_NEWLINE.sub("", line)
                line = PATTERN_SPACE_TAB.split(line)
                k = self.key_(line[0])
                F = int(math.log(float(line[1]) / self.DENOMINATOR) + 0.5)
                if k not in self.trie_ or self.trie_[k][0] < F:
                    self.trie_[self.key_(line[0])] = (F, line[2])
                self.trie_[self.rkey_(line[0])] = 1

            dict_file_cache = fnm + ".trie"
            logging.info(f"[HUQIE]:Build trie cache to {dict_file_cache}")
            self.trie_.save(dict_file_cache)
            of.close()
        except Exception:
            logging.exception(f"[HUQIE]:Build trie {fnm} failed")

    def __init__(self, debug=False):
        self.DEBUG = debug
        self.DENOMINATOR = 1000000
        self.DIR_ = f"{_curr_dir}/../res/huqie"

        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

        trie_file_name = self.DIR_ + ".txt.trie"
        # check if trie file existence
        if os.path.exists(trie_file_name):
            try:
                # load trie from file
                self.trie_ = datrie.Trie.load(trie_file_name)
                return
            except Exception:
                # fail to load trie from file, build default trie
                logging.exception(f"[HUQIE]:Fail to load trie file {trie_file_name}, build the default trie file")
                self.trie_ = datrie.Trie(string.printable)
        else:
            # file not exist, build default trie
            logging.info(f"[HUQIE]:Trie file {trie_file_name} not found, build the default trie file")
            self.trie_ = datrie.Trie(string.printable)

        # load data from dict file and save to trie file
        self.loadDict_(self.DIR_ + ".txt")

    def loadUserDict(self, fnm):
        try:
            self.trie_ = datrie.Trie.load(fnm + ".trie")
            return
        except Exception:
            self.trie_ = datrie.Trie(string.printable)
        self.loadDict_(fnm)

    def addUserDict(self, fnm):
        self.loadDict_(fnm)

    def add_word(self, word, frequency: int = None, pos: str = None):
        F = int(math.log(float(frequency) / self.DENOMINATOR) + 0.5)
        key = self.key_(word)
        rkey = self.rkey_(word)
        self.trie_[key] = (F, pos)
        self.trie_[rkey] = 1

    def del_word(self, word):
        key = self.key_(word)
        rkey = self.rkey_(word)

        if key in self.trie_:
            del self.trie_[key]

        if rkey in self.trie_:
            del self.trie_[rkey]

    def update_word(self, word, frequency: int = None, pos: str = None):
        self.del_word(word)
        self.add_word(word, frequency, pos)

    def dfs_(self, chars, s, preTks, tkslist):
        res = s
        # if s > MAX_L or s>= len(chars):
        if s >= len(chars):
            tkslist.append(preTks)
            return res

        # pruning
        S = s + 1
        if s + 2 <= len(chars):
            t1, t2 = "".join(chars[s: s + 1]), "".join(chars[s: s + 2])
            if self.trie_.has_keys_with_prefix(self.key_(t1)) and not self.trie_.has_keys_with_prefix(self.key_(t2)):
                S = s + 2
        if (len(preTks) > 2 and len(preTks[-1][0]) == 1 and len(preTks[-2][0]) == 1 and len(preTks[-3][0]) == 1):
            t1 = preTks[-1][0] + "".join(chars[s: s + 1])
            if self.trie_.has_keys_with_prefix(self.key_(t1)):
                S = s + 2

        ################
        for e in range(S, len(chars) + 1):
            t = "".join(chars[s:e])
            k = self.key_(t)

            if e > s + 1 and not self.trie_.has_keys_with_prefix(k):
                break

            if k in self.trie_:
                pretks = copy.deepcopy(preTks)
                if k in self.trie_:
                    pretks.append((t, self.trie_[k]))
                else:
                    pretks.append((t, (-12, "")))
                res = max(res, self.dfs_(chars, e, pretks, tkslist))

        if res > s:
            return res

        t = "".join(chars[s: s + 1])
        k = self.key_(t)
        if k in self.trie_:
            preTks.append((t, self.trie_[k]))
        else:
            preTks.append((t, (-12, "")))

        return self.dfs_(chars, s + 1, preTks, tkslist)

    def freq(self, tk):
        k = self.key_(tk)
        if k not in self.trie_:
            return 0
        return int(math.exp(self.trie_[k][0]) * self.DENOMINATOR + 0.5)

    def tag(self, tk):
        k = self.key_(tk)
        if k not in self.trie_:
            return ""
        return self.trie_[k][1]

    def score_(self, tfts):
        B = 30
        F, L, tks = 0, 0, []
        for tk, (freq, tag) in tfts:
            F += freq
            L += 0 if len(tk) < 2 else 1
            tks.append(tk)
        # F /= len(tks)
        L /= len(tks)
        logging.debug("[SC] {} {} {} {} {}".format(tks, len(tks), L, F, B / len(tks) + L + F))
        return tks, B / len(tks) + L + F

    def sortTks_(self, tkslist):
        res = []
        for tfts in tkslist:
            tks, s = self.score_(tfts)
            res.append((tks, s))
        return sorted(res, key=lambda x: x[1], reverse=True)

    def merge_(self, tks):
        # if split chars is part of token
        res = []
        tks = PATTERN_SPACE.sub(" ", tks).split()
        s = 0
        while True:
            if s >= len(tks):
                break
            E = s + 1
            for e in range(s + 2, min(len(tks) + 2, s + 6)):
                tk = "".join(tks[s:e])
                if PATTERN_SPLIT_CHARS.search(tk) and self.freq(tk):
                    E = e
            res.append("".join(tks[s:E]))
            s = E

        return " ".join(res)

    def maxForward_(self, line):
        res = []
        s = 0
        while s < len(line):
            e = s + 1
            t = line[s:e]
            while e < len(line) and self.trie_.has_keys_with_prefix(self.key_(t)):
                e += 1
                t = line[s:e]

            while e - 1 > s and self.key_(t) not in self.trie_:
                e -= 1
                t = line[s:e]

            if self.key_(t) in self.trie_:
                res.append((t, self.trie_[self.key_(t)]))
            else:
                res.append((t, (0, "")))

            s = e

        return self.score_(res)

    def maxBackward_(self, line):
        res = []
        s = len(line) - 1
        while s >= 0:
            e = s + 1
            t = line[s:e]
            while s > 0 and self.trie_.has_keys_with_prefix(self.rkey_(t)):
                s -= 1
                t = line[s:e]

            while s + 1 < e and self.key_(t) not in self.trie_:
                s += 1
                t = line[s:e]

            if self.key_(t) in self.trie_:
                res.append((t, self.trie_[self.key_(t)]))
            else:
                res.append((t, (0, "")))

            s -= 1

        return self.score_(res[::-1])

    def english_normalize_(self, tks):
        return [(self.stemmer.stem(self.lemmatizer.lemmatize(t)) if PATTERN_ALPHA_UNDERSCORE_HYPHEN.match(t) else t) for
                t in tks]

    def tokenize(self, line):
        line = PATTERN_NON_WORD_CHARS.sub(" ", line)
        line = strQ2B(line).lower()
        line = tradi2simp(line)
        zh_num = len([1 for c in line if is_chinese(c)])
        if zh_num == 0:
            return " ".join([self.stemmer.stem(self.lemmatizer.lemmatize(t)) for t in word_tokenize(line)])

        arr = PATTERN_SPLIT_CHARS.split(line)
        res = []
        for L in arr:
            if len(L) < 2 or PATTERN_LOWERCASE_DOT_HYPHEN.match(L) or PATTERN_NUMERIC_PERIOD_HYPHEN.match(L):
                res.append(L)
                continue
            # print(L)

            # use maxforward for the first time
            tks, s = self.maxForward_(L)
            tks1, s1 = self.maxBackward_(L)
            if self.DEBUG:
                logging.debug("[FW] {} {}".format(tks, s))
                logging.debug("[BW] {} {}".format(tks1, s1))

            i, j, _i, _j = 0, 0, 0, 0
            same = 0
            while i + same < len(tks1) and j + same < len(tks) and tks1[i + same] == tks[j + same]:
                same += 1
            if same > 0:
                res.append(" ".join(tks[j: j + same]))
            _i = i + same
            _j = j + same
            j = _j + 1
            i = _i + 1

            while i < len(tks1) and j < len(tks):
                tk1, tk = "".join(tks1[_i:i]), "".join(tks[_j:j])
                if tk1 != tk:
                    if len(tk1) > len(tk):
                        j += 1
                    else:
                        i += 1
                    continue

                if tks1[i] != tks[j]:
                    i += 1
                    j += 1
                    continue
                # backward tokens from_i to i are different from forward tokens from _j to j.
                tkslist = []
                self.dfs_("".join(tks[_j:j]), 0, [], tkslist)
                res.append(" ".join(self.sortTks_(tkslist)[0][0]))

                same = 1
                while i + same < len(tks1) and j + same < len(tks) and tks1[i + same] == tks[j + same]:
                    same += 1
                res.append(" ".join(tks[j: j + same]))
                _i = i + same
                _j = j + same
                j = _j + 1
                i = _i + 1

            if _i < len(tks1):
                assert _j < len(tks)
                assert "".join(tks1[_i:]) == "".join(tks[_j:])
                tkslist = []
                self.dfs_("".join(tks[_j:]), 0, [], tkslist)
                res.append(" ".join(self.sortTks_(tkslist)[0][0]))

        res = " ".join(self.english_normalize_(res))
        logging.debug("[TKS] {}".format(self.merge_(res)))
        return self.merge_(res)

    def fine_grained_tokenize(self, tks):
        tks = tks.split()
        zh_num = len([1 for c in tks if c and is_chinese(c[0])])
        if zh_num < len(tks) * 0.2:
            res = []
            for tk in tks:
                res.extend(tk.split("/"))
            return " ".join(res)

        res = []
        for tk in tks:
            if len(tk) < 3 or PATTERN_NUMERIC_COMMA_DOT_HYPHEN.match(tk):
                res.append(tk)
                continue
            tkslist = []
            if len(tk) > 10:
                tkslist.append(tk)
            else:
                self.dfs_(tk, 0, [], tkslist)
            if len(tkslist) < 2:
                res.append(tk)
                continue
            stk = self.sortTks_(tkslist)[1][0]
            if len(stk) == len(tk):
                stk = tk
            else:
                if PATTERN_LOWERCASE_DOT_HYPHEN.match(tk):
                    for t in stk:
                        if len(t) < 3:
                            stk = tk
                            break
                    else:
                        stk = " ".join(stk)
                else:
                    stk = " ".join(stk)

            res.append(stk)

        return " ".join(self.english_normalize_(res))


def is_chinese(s):
    if s >= "\u4e00" and s <= "\u9fa5":
        return True
    else:
        return False


def is_number(s):
    if s >= "\u0030" and s <= "\u0039":
        return True
    else:
        return False


def is_alphabet(s):
    if (s >= "\u0041" and s <= "\u005a") or (s >= "\u0061" and s <= "\u007a"):
        return True
    else:
        return False


def naiveQie(txt):
    tks = []
    for t in txt.split():
        if tks and PATTERN_ENDS_WITH_LETTER.match(tks[-1]) and PATTERN_ENDS_WITH_LETTER.match(t):
            tks.append(" ")
        tks.append(t)
    return tks
