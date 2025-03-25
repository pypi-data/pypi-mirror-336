from abc import ABC, abstractmethod
from typing import List
from indiquo.match.Match import Match


class IndiQuoBase(ABC):

    @abstractmethod
    def compare(self, target_text: str) -> List[Match]:
        pass
