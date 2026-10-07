import pytest

from hello_jev.game import Answer, Game, GameOverError, interpret


class FakeOracle:
    def __init__(self, ask: float = 0.9, same: float = 0.0) -> None:
        self.ask_probability = ask
        self.same_probability = same
        self.asked: list[tuple[str, str]] = []

    def ask(self, secret: str, question: str) -> float:
        self.asked.append((secret, question))
        return self.ask_probability

    def is_same(self, secret: str, guess: str) -> float:
        return self.same_probability


@pytest.mark.parametrize(
    ("probability", "expected"),
    [
        (0.98, Answer.YES),
        (0.61, Answer.YES),
        (0.6, Answer.UNSURE),
        (0.5, Answer.UNSURE),
        (0.4, Answer.UNSURE),
        (0.39, Answer.NO),
        (0.02, Answer.NO),
    ],
)
def test_確率が40から60パーセントのときは微妙と答える(probability, expected):
    assert interpret(probability) is expected


def test_質問するとお題と質問がoracleに渡り確率つきで答えが返る():
    oracle = FakeOracle(ask=0.91)
    game = Game("ペンギン", oracle)

    reply = game.ask("鳥ですか？")

    assert oracle.asked == [("ペンギン", "鳥ですか？")]
    assert reply.answer is Answer.YES
    assert reply.probability == 0.91


def test_質問するたびに残り回数が減る():
    game = Game("ペンギン", FakeOracle(), max_questions=20)

    game.ask("生き物ですか？")
    game.ask("飛びますか？")

    assert game.remaining == 18


def test_お題と同じものを答えると勝ちになる():
    game = Game("ペンギン", FakeOracle(same=0.95))

    assert game.guess("ぺんぎん") is True
    assert game.won is True
    assert game.is_over is True


def test_外れた答えも1問として数えゲームは続く():
    game = Game("ペンギン", FakeOracle(same=0.1), max_questions=20)

    assert game.guess("アザラシ") is False
    assert game.remaining == 19
    assert game.is_over is False


def test_残り回数を使い切ると負けで終わる():
    game = Game("ペンギン", FakeOracle(), max_questions=2)

    game.ask("生き物ですか？")
    game.ask("飛びますか？")

    assert game.is_over is True
    assert game.won is False


def test_終わったゲームには質問できない():
    game = Game("ペンギン", FakeOracle(same=0.95))
    game.guess("ペンギン")

    with pytest.raises(GameOverError):
        game.ask("生き物ですか？")
