import json
import logging
import math
import os
import re
from dataclasses import dataclass
from typing import Set

import numpy as np

from duowen_huqie.nlp.rag_tokenizer import RagTokenizer
from .re_pattern import (PATTERN_NUMERIC_COMMA_DOT_END, PATTERN_SHORT_ALPHA, PATTERN_NUMERIC_HYPHEN, PATTERN_ENGLISH_CHARS, PATTERN_SPECIAL_NUMERIC, PATTERN_ENDS_WITH_LETTER,
                         PATTERN_DIGIT_END, PATTERN_SHORT_ALNUM, PATTERN_ALNUM, PATTERN_WHITESPACE,
                         PATTERN_SPECIAL_CHARS)
from .stopwords import STOPWORDS

_curr_dir = os.path.dirname(os.path.abspath(__file__))


@dataclass(frozen=True, kw_only=True)
class TermDefine:
    weight: int
    desc: str


class TermInfo:
    toxic: TermDefine = TermDefine(weight=2, desc="有毒实体")
    func: TermDefine = TermDefine(weight=1, desc="功能实体")
    corp: TermDefine = TermDefine(weight=3, desc="公司实体")
    sch: TermDefine = TermDefine(weight=3, desc="学校实体")
    stock: TermDefine = TermDefine(weight=3, desc="股票实体")
    firstnm: TermDefine = TermDefine(weight=1, desc="名字实体")
    # 新增
    time: TermDefine = TermDefine(weight=1, desc="时间实体")
    product: TermDefine = TermDefine(weight=1, desc="产品实体")
    event: TermDefine = TermDefine(weight=1, desc="事件实体")
    org: TermDefine = TermDefine(weight=1, desc="组织实体")
    tech: TermDefine = TermDefine(weight=1, desc="技术实体")
    law: TermDefine = TermDefine(weight=1, desc="法律实体")

    def __init__(self):
        self.__term_type: Set[str] = {'toxic', 'func', 'corp', 'sch', 'stock', 'firstnm', 'time', 'product', 'event',
                                      'org', 'tech', 'law'}
        self.__desc_dict = {self.__getattribute__(attr_name).desc: attr_name for attr_name in self.__term_type if
                            not attr_name.startswith("__")}
        self.__word_dict = {attr_name: self.__getattribute__(attr_name).weight for attr_name in self.__term_type if
                            not attr_name.startswith("__")}

    # 提供给 term_weight使用，老代码保持不变
    def __getitem__(self, item):
        return self.__word_dict[item]

    def __setitem__(self, key, value):
        raise NotImplemented(f"不支持的方法")

    def __setattr__(self, key: str, value):
        if key[-11:] not in {"__word_dict", "__desc_dict", "__term_type"}:
            raise NotImplemented(f"不支持的方法")
        super().__setattr__(key, value)

    def get_all_term_type(self) -> Set[str]:
        return self.__term_type

    def get_all_term_desc(self) -> Set[str]:
        return set(self.__desc_dict.keys())

    def get_desc_by_name(self, term: str) -> str:
        return self.__getattribute__(term).desc

    def get_name_by_desc(self, desc: str) -> str:
        return self.__desc_dict[desc]


class TermWeightDealer:
    def __init__(self, tokenizer: RagTokenizer):

        self.tokenizer = tokenizer
        self.stop_words = STOPWORDS
        self.__term_info = TermInfo()
        self.ne, self.df = {}, {}
        self.init_word()

    def init_word(self):
        def load_dict(fnm):
            res = {}
            with open(fnm, "r") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    arr = line.replace("\n", "").split("\t")
                    if len(arr) < 2:
                        res[arr[0]] = 0
                    else:
                        res[arr[0]] = int(arr[1])

                c = 0
                for _, v in res.items():
                    c += v
                if c == 0:
                    return set(res.keys())
                return res

        fnm = f"{_curr_dir}/../res"
        self.ne, self.df = {}, {}
        try:
            with open(os.path.join(fnm, "ner.json"), "r") as ner_reader:
                self.ne = json.load(ner_reader)
        except Exception:
            logging.warning("Load ner.json FAIL!")
        try:
            if os.path.exists(os.path.join(fnm, "term.freq")):
                self.df = load_dict(os.path.join(fnm, "term.freq"))
        except Exception:
            logging.warning("Load term.freq FAIL!")

    def set_word(self, word: str, term_type: str) -> None:
        if term_type not in self.__term_info.get_all_term_desc():
            raise ValueError(f"类型 {type} 没有定义权重")
        self.ne[word] = self.__term_info.get_name_by_desc(term_type)

    def del_word(self, word: str) -> None:
        if word in self.ne:
            _ = self.ne.pop(word)

    def pretoken(self, txt, num=False, stpwd=True):
        patt = [PATTERN_SPECIAL_CHARS]
        rewt = []
        for p, r in rewt:
            txt = re.sub(p, r, txt)

        res = []
        for t in self.tokenizer.tokenize(txt).split():
            tk = t
            if (stpwd and tk in self.stop_words) or (PATTERN_DIGIT_END.match(tk) and not num):
                continue
            for p in patt:
                if p.match(t):
                    tk = "#"
                    break
            # tk = re.sub(r"([\+\\-])", r"\\\1", tk)
            if tk != "#" and tk:
                res.append(tk)
        return res

    def tokenMerge(self, tks):
        def oneTerm(t):
            return len(t) == 1 or PATTERN_SHORT_ALNUM.match(t)

        res, i = [], 0
        while i < len(tks):
            j = i
            if (i == 0 and oneTerm(tks[i]) and len(tks) > 1 and (
                    len(tks[i + 1]) > 1 and not PATTERN_ALNUM.match(tks[i + 1]))):  # 多 工位
                res.append(" ".join(tks[0:2]))
                i = 2
                continue

            while (j < len(tks) and tks[j] and tks[j] not in self.stop_words and oneTerm(tks[j])):
                j += 1
            if j - i > 1:
                if j - i < 5:
                    res.append(" ".join(tks[i:j]))
                    i = j
                else:
                    res.append(" ".join(tks[i: i + 2]))
                    i = i + 2
            else:
                if len(tks[i]) > 0:
                    res.append(tks[i])
                i += 1
        return [t for t in res if t]

    def ner(self, t):
        if not self.ne:
            return ""
        res = self.ne.get(t, "")
        if res:
            return res

    def split(self, txt):
        tks = []
        for t in PATTERN_WHITESPACE.sub(" ", txt).split():
            if (tks and PATTERN_ENDS_WITH_LETTER.match(tks[-1]) and PATTERN_ENDS_WITH_LETTER.match(t) and tks and self.ne.get(t,
                                                                                                                      "") != "func" and self.ne.get(
                tks[-1], "") != "func"):
                tks[-1] = tks[-1] + " " + t
            else:
                tks.append(t)
        return tks

    def weights(self, tks, preprocess=True):

        def ner(t):
            """
            "toxic": 代表有毒的或有害的实体，权重为 2。
            "func": 代表功能或函数实体，权重为 1。
            "corp": 代表公司实体，权重为 3。
            "loca": 代表地点或位置实体，权重为 3。
            "sch": 代表学校实体，权重为 3。
            "stock": 代表股票实体，权重为 3。
            "firstnm": 代表名字实体，权重为 1。
            """
            if PATTERN_NUMERIC_COMMA_DOT_END.match(t):
                return 2
            if PATTERN_SHORT_ALPHA.match(t):
                return 0.01
            if not self.ne or t not in self.ne:
                return 1
            return self.__term_info[self.ne[t]]

        def postag(t):
            t = self.tokenizer.tag(t)
            if t in {"r", "c", "d"}:
                return 0.3
            if t in {"ns", "nt"}:
                return 3
            if t in {"n"}:
                return 2
            if PATTERN_NUMERIC_HYPHEN.match(t):
                return 2
            return 1

        def freq(t):
            if PATTERN_SPECIAL_NUMERIC.match(t):
                return 3
            s = self.tokenizer.freq(t)
            if not s and PATTERN_ENGLISH_CHARS.match(t):
                return 300
            if not s:
                s = 0

            if not s and len(t) >= 4:
                s = [tt for tt in self.tokenizer.fine_grained_tokenize(t).split() if len(tt) > 1]
                if len(s) > 1:
                    s = np.min([freq(tt) for tt in s]) / 6.0
                else:
                    s = 0

            return max(s, 10)

        def df(t):
            if PATTERN_SPECIAL_NUMERIC.match(t):
                return 5
            if t in self.df:
                return self.df[t] + 3
            elif PATTERN_ENGLISH_CHARS.match(t):
                return 300
            elif len(t) >= 4:
                s = [tt for tt in self.tokenizer.fine_grained_tokenize(t).split() if len(tt) > 1]
                if len(s) > 1:
                    return max(3, np.min([df(tt) for tt in s]) / 6.0)

            return 3

        def idf(s, N):
            return math.log10(10 + ((N - s + 0.5) / (s + 0.5)))

        tw = []
        if not preprocess:
            idf1 = np.array([idf(freq(t), 10000000) for t in tks])
            idf2 = np.array([idf(df(t), 1000000000) for t in tks])
            wts = (0.3 * idf1 + 0.7 * idf2) * np.array([ner(t) * postag(t) for t in tks])
            wts = [s for s in wts]
            tw = list(zip(tks, wts))
        else:
            for tk in tks:
                tt = self.tokenMerge(self.pretoken(tk, True))
                idf1 = np.array([idf(freq(t), 10000000) for t in tt])
                idf2 = np.array([idf(df(t), 1000000000) for t in tt])
                wts = (0.3 * idf1 + 0.7 * idf2) * np.array([ner(t) * postag(t) for t in tt])
                wts = [s for s in wts]
                tw.extend(zip(tt, wts))

        S = np.sum([s for _, s in tw])
        return [(t, s / S) for t, s in tw]
