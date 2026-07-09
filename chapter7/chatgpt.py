import os

from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("環境変数 OPENAI_API_KEY を設定してください。")

client = OpenAI(api_key=OPENAI_API_KEY)

response = client.responses.create(
    model="gpt-5.4-nano",
    input="夜寝る前にちょうどいい一角獣（ユニコーン）が登場する物語を作ってください。",
)

print(response.output_text)
