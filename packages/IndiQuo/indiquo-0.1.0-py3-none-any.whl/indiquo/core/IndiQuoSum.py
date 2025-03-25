from typing import List

from indiquo.core.CandidatePredictorSum import CandidatePredictorSum
from indiquo.core.CandidateWithScenes import CandidateWithScenes
from indiquo.core.IndiQuoBase import IndiQuoBase
from indiquo.match.Match import Match


# noinspection PyMethodMayBeStatic
class IndiQuoSum(IndiQuoBase):

    def __init__(self, candidate_predictor: CandidatePredictorSum):
        self.candidate_predictor = candidate_predictor

    def compare(self, target_text: str) -> List[Match]:
        result: List[Match] = []
        candidates: List[CandidateWithScenes] = self.candidate_predictor.get_candidates(target_text)

        for candidate in candidates:
            result.append(Match(candidate.start, candidate.end, candidate.text, candidate.score,
                                candidate.scene_predictions))

        return result
