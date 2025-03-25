from dataclasses import dataclass
from typing import List
from indiquo.core.ScenePrediction import ScenePrediction


@dataclass
class Match:
    target_start: int
    target_end: int
    target_text: str
    score: float
    scene_predictions: List[ScenePrediction]
