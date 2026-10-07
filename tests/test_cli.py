import pytest

from hello_jev.cli import play
from hello_jev.game import Game


class ScriptedOracle:
    def __init__(self, asks: list[float], same: float = 0.0) -> None:
        self._asks = iter(asks)
        self._same = same
        self.questions: list[str] = []

    def ask(self, secret: str, question: str) -> float:
        self.questions.append(question)
        return next(self._asks)

    def is_same(self, secret: str, guess: str) -> float:
        return self._same


def run(game: Game, inputs: list[str]) -> str:
    lines = iter(inputs)
    output: list[str] = []
    play(game, read=lambda _prompt: next(lines), write=output.append)
    return "\n".join(output)


def test_質問への答えを確率つきで表示する():
    game = Game("ペンギン", ScriptedOracle(asks=[0.98], same=0.9))

    output = run(game, ["生き物ですか？", "答え：ペンギン"])

    assert "はい (98%)" in output


@pytest.mark.parametrize("line", ["答え：ペンギン", "答え:ペンギン", "答え ペンギン"])
def test_答えで始まる入力は質問ではなく回答として扱う(line):
    oracle = ScriptedOracle(asks=[], same=0.9)
    game = Game("ペンギン", oracle)

    output = run(game, [line])

    assert oracle.questions == []
    assert "正解" in output
    assert "1問" in output


def test_空行は質問として数えない():
    game = Game("ペンギン", ScriptedOracle(asks=[], same=0.9))

    run(game, ["", "答え：ペンギン"])

    assert game.remaining == 19


def test_使い切ったらお題を明かして終わる():
    game = Game("ペンギン", ScriptedOracle(asks=[0.1]), max_questions=1)

    output = run(game, ["空を飛びますか？"])

    assert "ペンギン" in output
    assert "残念" in output
