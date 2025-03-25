from typing import List

from indiquo.core.BaseCandidatePredictor import BaseCandidatePredictor
from indiquo.core.BaseScenePredictor import BaseScenePredictor
from indiquo.core.Candidate import Candidate
from indiquo.core.IndiQuoBase import IndiQuoBase
from indiquo.match.Match import Match


# noinspection PyMethodMayBeStatic
class IndiQuo(IndiQuoBase):

    def __init__(self, candidate_predictor: BaseCandidatePredictor, scene_predictor: BaseScenePredictor):
        self.candidate_predictor = candidate_predictor
        self.scene_predictor = scene_predictor

    def compare(self, target_text: str) -> List[Match]:
        result: List[Match] = []
        candidates: List[Candidate] = self.candidate_predictor.get_candidates(target_text)
        scene_predictions_list = self.scene_predictor.predict_scene([x.text for x in candidates])

        for candidate, scene_predictions in zip(candidates, scene_predictions_list):
            result.append(Match(candidate.start, candidate.end, candidate.text, candidate.score, scene_predictions))

        return result
