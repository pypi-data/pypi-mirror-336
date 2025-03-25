from typing import List, Tuple
from indiquo.core.CandidateWithScenes import CandidateWithScenes
from indiquo.core.ScenePrediction import ScenePrediction
from indiquo.core.chunker.BaseChunker import BaseChunker
from kpcommons.Footnote import map_to_real_pos, get_footnote_ranges, remove_footnotes
from sentence_transformers import util, SentenceTransformer


# noinspection PyMethodMayBeStatic
class CandidatePredictorSum:

    def __init__(self, summaries: List[Tuple[int, int, str]], model: SentenceTransformer, chunker: BaseChunker):
        self.summaries = summaries
        self.model = model
        self.chunker = chunker
        self.summary_embeddings = model.encode([x[2] for x in self.summaries], convert_to_tensor=True)

    def get_candidates(self, target_text: str) -> List[CandidateWithScenes]:
        fn_ranges, fn_ranges_with_offset = get_footnote_ranges(target_text)
        target_text_wo_fn: str = remove_footnotes(target_text)
        chunks = self.chunker.chunk(target_text_wo_fn)

        for chunk in chunks:
            start = chunk.start
            end = chunk.end
            real_start, real_end = map_to_real_pos(start, end, fn_ranges_with_offset)
            chunk.start = real_start
            chunk.end = real_end

        sentences = [x.text for x in chunks]
        scores, scene_predictions_list = self.__predict(sentences)

        candidates: List[CandidateWithScenes] = []

        for chunk, score, scene_predictions in zip(chunks, scores, scene_predictions_list):
            candidates.append(CandidateWithScenes(chunk.start, chunk.end, chunk.text, score, scene_predictions))

        return candidates

    def __predict(self, sentences: List[str]) -> Tuple[List[float], List[List[ScenePrediction]]]:
        target_embedding = self.model.encode(sentences, convert_to_tensor=True)
        hits = util.semantic_search(target_embedding, self.summary_embeddings, top_k=10)

        scores = []
        scene_prediction_lists = []
        for hit in hits:
            score = hit[0]['score']
            scores.append(score)

            scene_predictions = []

            for k in hit:
                idx = k['corpus_id']
                score = k['score']
                act_nr = self.summaries[idx][0]
                scene_nr = self.summaries[idx][1]
                scene_predictions.append(ScenePrediction(act_nr, scene_nr, score))

            scene_prediction_lists.append(scene_predictions)

        return scores, scene_prediction_lists
