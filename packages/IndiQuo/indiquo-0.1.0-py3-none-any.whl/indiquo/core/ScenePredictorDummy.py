from typing import List

from indiquo.core.BaseScenePredictor import BaseScenePredictor
from indiquo.core.ScenePrediction import ScenePrediction


class ScenePredictorDummy(BaseScenePredictor):

    def predict_scene(self, text: str | List[str]) -> List[List[ScenePrediction]]:
        if isinstance(text, str):
            text = [text]

        result = [[] for _ in range(len(text))]
        return result
