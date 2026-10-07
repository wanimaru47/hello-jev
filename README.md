# hello-jev

Jev（TypeSafe AI）に出題者をさせて「20の質問」を遊ぶ CLI。

## 必要なもの

- Python 3.14 以上
- [uv](https://docs.astral.sh/uv/)
- TypeSafe の API キー（`.env` の `TYPESAFE_API_KEY`）

## 遊び方

```console
$ uv sync
$ cp .env.example .env    # TYPESAFE_API_KEY を書き換える
$ uv run --env-file .env hello-jev
お題を決めました。はい/いいえで答えられる質問をどうぞ（残り20問）
当てるときは「答え：〇〇」と入力してください
Q1> それは動物ですか？
  → はい (97%)
Q2> 海に住んでいますか？
  → いいえ (8%)
Q3> 答え：パンダ
  🎉 正解！ 3問で当たりました
```

- お題は動物の中からランダムに選ばれる
- はい/いいえで答えられる質問をすると、Jev が「はい」「いいえ」「微妙」と確率で答える
- 「答え：〇〇」で回答する。表記ゆれ（カタカナ・ひらがな・漢字・英語）は同じものとして判定される
- 質問と回答を合わせて 20 回以内に当てれば勝ち
- `Ctrl+C` / `Ctrl+D` で中断するとお題が表示される

## 開発

```console
$ uv run pytest          # テスト
$ uv run ruff check .    # lint
$ uv run ruff format .   # format
$ uv build               # build
```
