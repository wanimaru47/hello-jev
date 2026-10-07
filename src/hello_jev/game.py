from dataclasses import dataclass
from enum import Enum
from typing import Protocol

UNSURE_LOWER = 0.4
UNSURE_UPPER = 0.6
MATCH_THRESHOLD = 0.5


class Answer(Enum):
    YES = "はい"
    NO = "いいえ"
    UNSURE = "微妙"


def interpret(probability: float) -> Answer:
    if probability > UNSURE_UPPER:
        return Answer.YES
    if probability < UNSURE_LOWER:
        return Answer.NO
    return Answer.UNSURE


@dataclass(frozen=True)
class Reply:
    answer: Answer
    probability: float


class Oracle(Protocol):
    def ask(self, secret: str, question: str) -> float: ...

    def is_same(self, secret: str, guess: str) -> float: ...


class GameOverError(Exception):
    pass


class Game:
    def __init__(self, secret: str, oracle: Oracle, max_questions: int = 20) -> None:
        self.secret = secret
        self.max_questions = max_questions
        self.remaining = max_questions
        self.won = False
        self._oracle = oracle

    @property
    def used(self) -> int:
        return self.max_questions - self.remaining

    @property
    def is_over(self) -> bool:
        return self.won or self.remaining <= 0

    def ask(self, question: str) -> Reply:
        self._consume_turn()
        probability = self._oracle.ask(self.secret, question)
        return Reply(interpret(probability), probability)

    def guess(self, text: str) -> bool:
        self._consume_turn()
        self.won = self._oracle.is_same(self.secret, text) > MATCH_THRESHOLD
        return self.won

    def _consume_turn(self) -> None:
        if self.is_over:
            raise GameOverError
        self.remaining -= 1
