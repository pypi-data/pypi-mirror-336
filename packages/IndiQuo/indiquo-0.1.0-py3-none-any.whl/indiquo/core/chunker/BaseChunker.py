from abc import ABC, abstractmethod
from typing import List
from indiquo.core.chunker.Chunk import Chunk


class BaseChunker(ABC):

    @abstractmethod
    def chunk(self, text: str) -> List[Chunk]:
        pass
