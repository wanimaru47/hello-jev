import random
import re
import sys
from collections.abc import Callable

from typesafe_sdk import TypeSafeClient, TypeSafeError

from hello_jev.game import Game
from hello_jev.jev_oracle import JevOracle
from hello_jev.topics import TOPICS

GUESS_PATTERN = re.compile(r"^答え[：:\s]\s*(?P<guess>.+)$")


def play(game: Game, read: Callable[[str], str], write: Callable[[str], None]) -> None:
    write(
        f"お題を決めました。はい/いいえで答えられる質問をどうぞ（残り{game.remaining}問）"
    )
    write("当てるときは「答え：〇〇」と入力してください")

    while not game.is_over:
        line = read(f"Q{game.used + 1}> ").strip()
        if not line:
            continue

        if match := GUESS_PATTERN.match(line):
            if game.guess(match["guess"]):
                write(f"  🎉 正解！ {game.used}問で当たりました")
            else:
                write(f"  ✗ ちがいます（残り{game.remaining}問）")
            continue

        reply = game.ask(line)
        write(f"  → {reply.answer.value} ({reply.probability:.0%})")

    if not game.won:
        write(f"  残念！ お題は「{game.secret}」でした")


def main() -> None:
    try:
        client = TypeSafeClient()
    except TypeSafeError as error:
        sys.exit(str(error))

    with client:
        game = Game(random.choice(TOPICS), JevOracle(client))
        try:
            play(game, read=input, write=print)
        except EOFError, KeyboardInterrupt:
            print(f"\nお題は「{game.secret}」でした")
