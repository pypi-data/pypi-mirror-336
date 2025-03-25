from dataclasses import dataclass


@dataclass
class Chunk:
    start: int
    end: int
    text: str
