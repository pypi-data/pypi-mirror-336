import json
import logging

import numpy as np

from duowen_huqie.nlp.rag_tokenizer import RagTokenizer
from duowen_huqie.nlp.re_pattern import PATTERN_WHITESPACE, PATTERN_ALPHA_ONLY_END, \
    PATTERN_SPECIAL_CHARS_SPACE_QUOTES_CARET, PATTERN_SINGLE_LOWERCASE_ALNUM, PATTERN_STARTS_WITH_PLUS_OR_MINUS, \
    PATTERN_SPECIAL_CHARS_DOT_CARET_PLUS_PAREN_HYPHEN, PATTERN_ALNUM_SPECIAL_CHARS_END, \
    PATTERN_PUNCTUATION_AND_SPECIAL_CHARS, PATTERN_ESCAPE_CHAR, PATTERN_SPECIAL_SYMBOLS, PATTERN_STOPWORD, \
    PATTERN_SPECIAL_CHARACTERS
from duowen_huqie.nlp.synonym import SynonymDealer
from duowen_huqie.nlp.term_weight import TermWeightDealer
from duowen_huqie.utils import MatchTextExpr, tradi2simp, strQ2B, record_time


class FulltextQueryer:
    def __init__(self, tokenizer: RagTokenizer, tw: TermWeightDealer, syn: SynonymDealer):
        self.tw = tw
        self.syn = syn
        self.tokenizer = tokenizer
        self.query_fields = ["title_tks^10", "title_sm_tks^5", "important_kwd^30", "important_tks^20",
                             "question_tks^20", "content_ltks^2", "content_sm_ltks", ]

    @staticmethod
    def subSpecialChar(line):
        return PATTERN_SPECIAL_SYMBOLS.sub(r"\\\1", line).strip()

    @staticmethod
    def isChinese(line):
        arr = PATTERN_WHITESPACE.split(line)
        if len(arr) <= 3:
            return True
        e = 0
        for t in arr:
            if not PATTERN_ALPHA_ONLY_END.match(t):
                e += 1
        return e * 1.0 / len(arr) >= 0.7

    @staticmethod
    def rmWWW(txt):
        for pattern, replacement in PATTERN_STOPWORD:
            txt = pattern.sub(replacement, txt)
        return txt

    def question(self, txt, tbl="qa", min_match: float = 0.6):
        txt = PATTERN_SPECIAL_CHARACTERS.sub(" ", tradi2simp(strQ2B(txt.lower())), ).strip()
        txt = FulltextQueryer.rmWWW(txt)

        if not self.isChinese(txt):
            txt = FulltextQueryer.rmWWW(txt)
            tks = self.tokenizer.tokenize(txt).split()
            keywords = [t for t in tks if t]
            tks_w = self.tw.weights(tks, preprocess=False)
            tks_w = [(PATTERN_SPECIAL_CHARS_SPACE_QUOTES_CARET.sub("", tk), w) for tk, w in tks_w]
            tks_w = [(PATTERN_SINGLE_LOWERCASE_ALNUM.sub("", tk), w) for tk, w in tks_w if tk]
            tks_w = [(PATTERN_STARTS_WITH_PLUS_OR_MINUS.sub("", tk), w) for tk, w in tks_w if tk]
            tks_w = [(tk.strip(), w) for tk, w in tks_w if tk.strip()]
            syns = []
            for tk, w in tks_w:
                syn = self.syn.lookup(tk)
                syn = self.tokenizer.tokenize(" ".join(syn)).split()
                keywords.extend(syn)
                syn = ['"{}"^{:.4f}'.format(s, w / 4.0) for s in syn if s.strip()]
                syns.append(" ".join(syn))

            q = ["({}^{:.4f}".format(tk, w) + " {})".format(syn) for (tk, w), syn in zip(tks_w, syns) if
                 tk and not PATTERN_SPECIAL_CHARS_DOT_CARET_PLUS_PAREN_HYPHEN.match(tk)]
            for i in range(1, len(tks_w)):
                left, right = tks_w[i - 1][0].strip(), tks_w[i][0].strip()
                if not left or not right:
                    continue
                q.append('"%s %s"^%.4f' % (tks_w[i - 1][0], tks_w[i][0], max(tks_w[i - 1][1], tks_w[i][1]) * 2,))
            if not q:
                q.append(txt)
            query = " ".join(q)
            return MatchTextExpr(self.query_fields, query, 100), keywords

        def need_fine_grained_tokenize(tk):
            if len(tk) < 3:
                return False
            if PATTERN_ALNUM_SPECIAL_CHARS_END.match(tk):
                return False
            return True

        txt = FulltextQueryer.rmWWW(txt)
        qs, keywords = [], []
        for tt in self.tw.split(txt)[:256]:  # .split():
            if not tt:
                continue
            keywords.append(tt)
            twts = self.tw.weights([tt])
            syns = self.syn.lookup(tt)
            if syns and len(keywords) < 32:
                keywords.extend(syns)
            logging.debug(json.dumps(twts, ensure_ascii=False))
            tms = []
            for tk, w in sorted(twts, key=lambda x: x[1] * -1):
                sm = (self.tokenizer.fine_grained_tokenize(tk).split() if need_fine_grained_tokenize(tk) else [])
                sm = [PATTERN_PUNCTUATION_AND_SPECIAL_CHARS.sub("", m, ) for m in sm]
                sm = [FulltextQueryer.subSpecialChar(m) for m in sm if len(m) > 1]
                sm = [m for m in sm if len(m) > 1]

                if len(keywords) < 32:
                    keywords.append(PATTERN_ESCAPE_CHAR.sub("", tk))
                    keywords.extend(sm)

                tk_syns = self.syn.lookup(tk)
                tk_syns = [FulltextQueryer.subSpecialChar(s) for s in tk_syns]
                if len(keywords) < 32:
                    keywords.extend([s for s in tk_syns if s])
                tk_syns = [self.tokenizer.fine_grained_tokenize(s) for s in tk_syns if s]
                tk_syns = [f'"{s}"' if s.find(" ") > 0 else s for s in tk_syns]

                if len(keywords) >= 32:
                    break

                tk = FulltextQueryer.subSpecialChar(tk)
                if tk.find(" ") > 0:
                    tk = '"%s"' % tk
                if tk_syns:
                    tk = f"({tk} OR (%s)^0.2)" % " ".join(tk_syns)
                if sm:
                    tk = f'{tk} OR "%s" OR ("%s"~2)^0.5' % (" ".join(sm), " ".join(sm))
                if tk.strip():
                    tms.append((tk, w))

            tms = " ".join([f"({t})^{w}" for t, w in tms])

            if len(twts) > 1:
                tms += ' ("%s"~2)^1.5' % self.tokenizer.tokenize(tt)

            syns = " OR ".join(['"%s"' % self.tokenizer.tokenize(FulltextQueryer.subSpecialChar(s)) for s in syns])
            if syns:
                tms = f"({tms})^5 OR ({syns})^0.7"

            qs.append(tms)

        if qs:
            query = " OR ".join([f"({t})" for t in qs if t])
            return (MatchTextExpr(self.query_fields, query, 100, {"minimum_should_match": min_match}), keywords,)
        return None, keywords

    @staticmethod
    def vector_similarity(avec, bvecs):

        avec = np.asarray(avec)
        bvecs = np.asarray(bvecs)

        avec_norm = np.linalg.norm(avec)
        bvecs_norm = np.linalg.norm(bvecs, axis=1)

        sims = np.dot(bvecs, avec) / (bvecs_norm * avec_norm + 1e-9)  # 加入平滑项防止除零
        return sims

    def hybrid_similarity(self, avec, bvecs, atks, btkss, tkweight: float = 0.3, vtweight: float = 0.7):
        """
        混合相似度 avec、bvecs、atks 和 btkss，它们分别表示查询的向量表示、文档的向量表示、查询的分词结果以及文档的分词结果。
        :param avec: 询的向量表示
        :param bvecs: 文档的向量表示
        :param atks: 查询的分词结果
        :param btkss: 文档的分词结果
        :param tkweight: 文本相似度的权重
        :param vtweight: 向量相似度的权重
        :return: 混合相似度得分,文本相似度得分,向量相似度得分

        hybrid_similarity(ans_embd,
           ins_embd,
           rag_tokenizer.tokenize(ans).split(),
           rag_tokenizer.tokenize(inst).split())
        """
        # from sklearn.metrics.pairwise import cosine_similarity as CosineSimilarity
        # import numpy as np
        #
        # sims = CosineSimilarity([avec], bvecs)
        # tksim = self.token_similarity(atks, btkss)
        # return np.array(sims[0]) * vtweight + np.array(tksim) * tkweight, tksim, sims[0]

        # 计算向量相似度 (cosine similarity)
        sims = self.vector_similarity(avec, bvecs)

        # 计算文本相似度
        tksim = self.token_similarity(atks, btkss)

        return np.array(sims) * vtweight + np.array(tksim) * tkweight, tksim, sims

    def token_similarity(self, atks, btkss):
        def toDict(tks):
            d = {}
            if isinstance(tks, str):
                tks = tks.split()
            for t, c in self.tw.weights(tks, preprocess=False):
                if t not in d:
                    d[t] = 0
                d[t] += c
            return d

        atks = toDict(atks)
        btkss = [toDict(tks) for tks in btkss]
        return [self.similarity(atks, btks) for btks in btkss]

    def similarity(self, qtwt, dtwt):
        if isinstance(dtwt, type("")):
            dtwt = {t: w for t, w in self.tw.weights(self.tw.split(dtwt), preprocess=False)}
        if isinstance(qtwt, type("")):
            qtwt = {t: w for t, w in self.tw.weights(self.tw.split(qtwt), preprocess=False)}
        s = 1e-9
        for k, v in qtwt.items():
            if k in dtwt:
                s += v  # * dtwt[k]
        q = 1e-9
        for k, v in qtwt.items():
            q += v
        return s / q

    def paragraph(self, content_tks: str, keywords: list = [], keywords_topn=30):
        if isinstance(content_tks, str):
            content_tks = [c.strip() for c in content_tks.strip() if c.strip()]
        tks_w = self.tw.weights(content_tks, preprocess=False)

        keywords = [f'"{k.strip()}"' for k in keywords]
        for tk, w in sorted(tks_w, key=lambda x: x[1] * -1)[:keywords_topn]:
            tk_syns = self.syn.lookup(tk)
            tk_syns = [FulltextQueryer.subSpecialChar(s) for s in tk_syns]
            tk_syns = [self.tokenizer.fine_grained_tokenize(s) for s in tk_syns if s]
            tk_syns = [f'"{s}"' if s.find(" ") > 0 else s for s in tk_syns]
            tk = FulltextQueryer.subSpecialChar(tk)
            if tk.find(" ") > 0:
                tk = '"%s"' % tk
            if tk_syns:
                tk = f"({tk} OR (%s)^0.2)" % " ".join(tk_syns)
            if tk:
                keywords.append(f"{tk}^{w}")

        return MatchTextExpr(self.query_fields, " ".join(keywords), 100,
                             {"minimum_should_match": min(3, len(keywords) / 10)}, )
