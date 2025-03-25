from abc import ABC, abstractmethod
from typing import List
from indiquo.core.ScenePrediction import ScenePrediction


class BaseScenePredictor(ABC):

    @abstractmethod
    def predict_scene(self, text: str | List[str]) -> List[List[ScenePrediction]]:
        pass
