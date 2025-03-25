from typing import List

try:
    from flair.data import Sentence
    from flair.nn import Model
except ModuleNotFoundError:
    pass

from indiquo.core.BaseCandidatePredictor import BaseCandidatePredictor
from indiquo.core.Candidate import Candidate
from indiquo.core.chunker.BaseChunker import BaseChunker
from kpcommons.Footnote import map_to_real_pos, get_footnote_ranges, remove_footnotes


class CandidatePredictorRW(BaseCandidatePredictor):

    def __init__(self, model: Model, chunker: BaseChunker):
        self.model = model
        self.chunker = chunker

    # overriding abstract method
    def get_candidates(self, target_text: str) -> List[Candidate]:
        fn_ranges, fn_ranges_with_offset = get_footnote_ranges(target_text)
        target_text_wo_fn: str = remove_footnotes(target_text)
        chunks = self.chunker.chunk(target_text_wo_fn)
        flair_sentences = []

        for s in chunks:
            flair_sentence = Sentence(s.text, use_tokenizer=True, start_position=s.start)
            self.model.predict(flair_sentence)
            flair_sentences.append(flair_sentence)

        candidates: List[Candidate] = []

        for fs in flair_sentences:
            found = False
            for t in fs.tokens:
                if t.labels[0].value == 'reported':
                    found = True
                    break

            label = 0.0
            if found:
                label = 1.0

            real_start, real_end = map_to_real_pos(fs.start_pos, fs.end_pos, fn_ranges_with_offset)
            chunk_text = target_text[real_start:real_end]
            current_candidate = Candidate(real_start, real_end, chunk_text, label)
            candidates.append(current_candidate)

        return candidates
