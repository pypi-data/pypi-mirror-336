from typing import List
from sentence_transformers import util, SentenceTransformer
from dramatist.drama.Drama import Drama

from indiquo.core.BaseCandidatePredictor import BaseCandidatePredictor
from indiquo.core.Candidate import Candidate
from indiquo.core.IndiQuoException import IndiQuoException
from indiquo.core.chunker.BaseChunker import BaseChunker
from kpcommons.Footnote import map_to_real_pos, get_footnote_ranges, remove_footnotes
import re


# noinspection PyMethodMayBeStatic
class CandidatePredictorST(BaseCandidatePredictor):

    def __init__(self, drama: Drama, model: SentenceTransformer, chunker: BaseChunker, add_context: bool, max_length: int):
        self.model = model
        self.chunker = chunker
        self.all_text_blocks = []
        self.source_text_blocks = []
        self.add_context = add_context
        self.max_length = max_length

        for act_nr, act in enumerate(drama.acts):
            for scene_nr, scene in enumerate(act.scenes):
                text_blocks = scene.get_text_in_blocks(128)

                for tbt in text_blocks:
                    self.all_text_blocks.append((act_nr, scene_nr, tbt.text))
                    self.source_text_blocks.append(tbt.text)

        self.source_embeddings = model.encode(self.source_text_blocks, convert_to_tensor=True)

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

            if self.add_context:
                text = self.__add_context(chunk.text, target_text, chunk.start, chunk.end)
            else:
                text = chunk.text

            score = self.__predict(text)
            candidates.append(Candidate(chunk.start, chunk.end, chunk.text, score))

        return candidates

    def __predict(self, target_text: str) -> float:
        target_embedding = self.model.encode([target_text], convert_to_tensor=True)
        hits = util.semantic_search(target_embedding, self.source_embeddings, top_k=1)[0]
        return hits[0]['score']

    def __add_context(self, quote_text: str, text: str, quote_start: int, quote_end: int) -> str:
        rest_len = self.max_length - len(quote_text.split())

        if rest_len < 0:
            raise IndiQuoException(f'Quote is longer than max length: {quote_text}')

        text_before = text[:quote_start]
        text_after = text[quote_end:]

        text_before = text_before.replace('\n', ' ')
        text_before = text_before.replace('\t', ' ')

        text_after = text_after.replace('\n', ' ')
        text_after = text_after.replace('\t', ' ')

        text_before = re.sub(r'\[\[\[(?:.|\n)+?]]]', ' ', text_before)
        text_after = re.sub(r'\[\[\[(?:.|\n)+?]]]', ' ', text_after)

        parts_before = text_before.split()
        parts_after = text_after.split()

        parts_before_count = len(parts_before)
        parts_after_count = len(parts_after)

        count_before = min(round(rest_len / 2), parts_before_count)
        count_after = min(rest_len - count_before, parts_after_count)

        if count_before < 0 or count_after < 0:
            raise IndiQuoException(f'No characters left before or after: Count before: {count_before}, after: {count_after}')

        text_before = ' '.join(parts_before[-count_before:])
        text_after = ' '.join(parts_after[:count_after])

        ex_text = f'{text_before} {quote_text} {text_after}'
        return ex_text
