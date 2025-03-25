from typing import List

from indiquo.core.BaseCandidatePredictor import BaseCandidatePredictor
from indiquo.core.Candidate import Candidate
from indiquo.core.chunker.BaseChunker import BaseChunker
from kpcommons.Footnote import map_to_real_pos, get_footnote_ranges, remove_footnotes


# noinspection PyMethodMayBeStatic
class CandidatePredictorDummy(BaseCandidatePredictor):

    def __init__(self, chunker: BaseChunker):
        self.chunker = chunker

    # overriding abstract method
    def get_candidates(self, target_text: str) -> List[Candidate]:
        fn_ranges, fn_ranges_with_offset = get_footnote_ranges(target_text)
        target_text_wo_fn: str = remove_footnotes(target_text)
        chunks = self.chunker.chunk(target_text_wo_fn)

        for chunk in chunks:
            start = chunk.start
            end = chunk.end
            real_start, real_end = map_to_real_pos(start, end, fn_ranges_with_offset)
            chunk.start = real_start
            chunk.end = real_end

        candidates: List[Candidate] = []
        for chunk in chunks:
            candidates.append(Candidate(chunk.start, chunk.end, chunk.text, 0))

        return candidates
