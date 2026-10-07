import json

import httpx2
from typesafe_sdk import TypeSafeClient

from hello_jev.jev_oracle import JevOracle


def make_client(noul: float, captured: list[dict]) -> TypeSafeClient:
    def handler(request: httpx2.Request) -> httpx2.Response:
        body = json.loads(request.content)
        captured.append(body)
        name = next(iter(body["questions"]))
        return httpx2.Response(
            200,
            json={
                "model": "jev",
                "answers": {name: {"type": "noul", "noul": noul}},
                "usage": {"input_tokens": 1, "output_tokens": 1},
            },
        )

    return TypeSafeClient(api_key="test", transport=httpx2.MockTransport(handler))


def test_質問はお題をstateに入れたnoulとして送られ確率が返る():
    captured: list[dict] = []
    oracle = JevOracle(make_client(0.87, captured))

    probability = oracle.ask("ペンギン", "鳥ですか？")

    assert probability == 0.87
    assert captured[0]["state"] == {"secret": "ペンギン"}
    question = next(iter(captured[0]["questions"].values()))
    assert question["type"] == "noul"
    assert "鳥ですか？" in json.dumps(question["instructions"], ensure_ascii=False)


def test_正解判定はお題と回答が同じものを指すかをnoulで問う():
    captured: list[dict] = []
    oracle = JevOracle(make_client(0.96, captured))

    probability = oracle.is_same("ペンギン", "ぺんぎん")

    assert probability == 0.96
    assert captured[0]["state"] == {"secret": "ペンギン", "guess": "ぺんぎん"}
