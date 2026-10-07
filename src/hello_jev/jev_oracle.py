from typesafe_sdk import Noul, TypeSafeClient


class JevOracle:
    def __init__(self, client: TypeSafeClient) -> None:
        self._client = client

    def ask(self, secret: str, question: str) -> float:
        return self._noul(
            state={"secret": secret},
            instructions=(
                "You are answering a game of 20 questions about the secret thing. "
                f"Is the answer to this question yes for the secret? Question: {question}"
            ),
        )

    def is_same(self, secret: str, guess: str) -> float:
        return self._noul(
            state={"secret": secret, "guess": guess},
            instructions=(
                "Does the guess refer to the same thing as the secret? "
                "Ignore differences in writing system (katakana, hiragana, kanji, English) and minor variations."
            ),
        )

    def _noul(self, state: dict[str, str], instructions: str) -> float:
        response = self._client.system_one(
            state=state,
            questions={"answer": Noul(instructions=instructions)},
        )
        return response.nouls["answer"].noul
