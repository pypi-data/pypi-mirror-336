from dataclasses import dataclass
from typing import List

from indiquo.core.ScenePrediction import ScenePrediction


@dataclass
class CandidateWithScenes:
    start: int
    end: int
    text: str
    score: float
    scene_predictions: List[ScenePrediction]
