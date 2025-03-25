from dataclasses import dataclass


@dataclass
class Candidate:
    start: int
    end: int
    text: str
    score: float
