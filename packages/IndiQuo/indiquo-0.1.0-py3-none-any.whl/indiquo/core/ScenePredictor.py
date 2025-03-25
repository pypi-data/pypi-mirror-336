from typing import List

from dramatist.drama.Drama import Drama
from sentence_transformers import util

from indiquo.core.BaseScenePredictor import BaseScenePredictor
from indiquo.core.ScenePrediction import ScenePrediction


class ScenePredictor(BaseScenePredictor):

    def __init__(self, drama: Drama, model, top_k: int):
        self.model = model
        self.top_k = top_k
        self.all_text_blocks = []

        source_text_blocks = []

        for act_nr, act in enumerate(drama.acts):
            for scene_nr, scene in enumerate(act.scenes):
                text_blocks = scene.get_text_in_blocks(128)

                for tbt in text_blocks:
                    self.all_text_blocks.append((act_nr+1, scene_nr+1, tbt.text))
                    source_text_blocks.append(tbt.text)

        self.source_embeddings = model.encode(source_text_blocks, convert_to_tensor=True)

    # overriding abstract method
    def predict_scene(self, text: str | List[str]) -> List[List[ScenePrediction]]:
        if isinstance(text, str):
            text = [text]

        target_embedding = self.model.encode(text, convert_to_tensor=True)
        hits = util.semantic_search(target_embedding, self.source_embeddings, top_k=self.top_k)

        predictions_list = []
        for hit in hits:
            scene_predictions = []
            for k in hit:
                idx = k['corpus_id']
                score = k['score']
                act_nr = self.all_text_blocks[idx][0]
                scene_nr = self.all_text_blocks[idx][1]
                scene_predictions.append(ScenePrediction(act_nr, scene_nr, score))

            predictions_list.append(scene_predictions)

        return predictions_list
