from functools import partial
from typing import List

from duowen_huqie.utils import record_time
from .query import FulltextQueryer
from .rag_tokenizer import RagTokenizer
from .synonym import SynonymDealer
from .term_weight import TermWeightDealer, TermInfo


class NLP:

    def __init__(self, tokenizer: RagTokenizer = None, tw: TermWeightDealer = None, syn: SynonymDealer = None):

        self.tokenizer = tokenizer if tokenizer else RagTokenizer()
        self.tw = tw if tw else TermWeightDealer(self.tokenizer)
        self.syn = syn if syn else SynonymDealer()
        self.query = FulltextQueryer(self.tokenizer, self.tw, self.syn)

        self.query_text_similarity = partial(self.text_similarity, qa=True)
        self.query_hybrid_similarity = partial(self.hybrid_similarity, qa=True)
        self.query_hybrid_similarity_with_all = partial(self.hybrid_similarity_with_all, qa=True)
        self.new_word = {}

    def tok_add_word(self, word, frequency: int, pos: str):
        self.tokenizer.add_word(word, frequency=frequency, pos=pos)
        self.new_word[word] = dict(frequency=frequency, pos=pos)

    def tok_del_word(self, word):
        self.tokenizer.del_word(word)
        if word in self.new_word:
            del self.new_word[word]

    def tok_tag_word(self, word):
        return self.tokenizer.tag(word)

    def tok_update_word(self, word, frequency: int, pos: str):
        self.tokenizer.update_word(word, frequency=frequency, pos=pos)
        self.new_word[word] = dict(frequency=frequency, pos=pos)

    def ner_init_word(self) -> None:
        self.tw.init_word()

    def ner_set_word(self, word: str, term_type: str) -> None:
        self.tw.set_word(word, term_type)

    def ner_del_word(self, word: str) -> None:
        self.tw.del_word(word)

    def syn_init_word(self) -> None:
        self.syn.init_word()

    def syn_set_word(self, word: str, alias: str) -> None:
        self.syn.set_word(word, alias)

    def syn_del_word(self, word: str) -> None:
        self.syn.del_word(word)

    def content_cut(self, text: str):
        return self.tokenizer.tokenize(text)

    def content_sm_cut(self, text: str):
        return self.tokenizer.fine_grained_tokenize(self.tokenizer.tokenize(text))

    def content_cut_for_search(self, text: str):
        return self.tokenizer.cut_for_search(text)

    def term_weight(self, text: str):
        match, keywords = self.query.question(text)
        if match:
            return match.matching_text
        else:
            return None

    @record_time()
    def text_similarity(self, question: str, docs: List[str] = None, docs_sm: List[str] = None, qa=False):
        if docs_sm is None and docs is None:
            raise Exception("docs_sm or docs need to be set")
        return [float(i) for i in
                self.query.token_similarity(self.content_cut(self.query.rmWWW(question) if qa else question),
                                            docs_sm if docs_sm else [self.content_cut(i) for i in docs])]

    @record_time()
    def hybrid_similarity_with_all(self, question: str, question_vector: List[float], docs_vector: List[List[float]],
                                   docs: List[str] = None, docs_sm: List[str] = None, tkweight: float = 0.3,
                                   vtweight: float = 0.7, qa=False):
        if docs_sm is None and docs is None:
            raise Exception("docs_sm or docs need to be set")
        _h, _t, _v = self.query.hybrid_similarity(question_vector, docs_vector,
                                                  self.content_cut(self.query.rmWWW(question) if qa else question),
                                                  docs_sm if docs_sm else [self.content_cut(i) for i in docs], tkweight,
                                                  vtweight)
        return [float(i) for i in _h], [float(i) for i in _t], [float(i) for i in _v]

    def hybrid_similarity(self, question: str, question_vector: List[float], docs_vector: List[List[float]],
                          docs: List[str] = None, docs_sm: List[str] = None, tkweight: float = 0.3,
                          vtweight: float = 0.7, qa=False):
        _h, _t, _v = self.hybrid_similarity_with_all(question, question_vector, docs_vector, docs, docs_sm, tkweight,
                                                     vtweight, qa=qa)
        return _h

    @record_time()
    def vector_similarity(self, question_vector: List[float], docs_vector: List[List[float]]):
        return [float(i) for i in self.query.vector_similarity(question_vector, docs_vector)]
