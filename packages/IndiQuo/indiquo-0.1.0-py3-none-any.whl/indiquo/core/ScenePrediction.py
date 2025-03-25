from dataclasses import dataclass


@dataclass
class ScenePrediction:
    act: int
    scene: int
    score: float
