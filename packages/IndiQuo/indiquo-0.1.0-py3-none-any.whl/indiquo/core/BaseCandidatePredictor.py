from abc import ABC, abstractmethod
from typing import List
from indiquo.core.Candidate import Candidate


class BaseCandidatePredictor(ABC):

    @abstractmethod
    def get_candidates(self, target_text: str) -> List[Candidate]:
        pass
