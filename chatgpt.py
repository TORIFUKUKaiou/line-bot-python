import os
from openai import OpenAI
# export OPENAI_API_KEY="My API Key"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {
            "role": "user",
            "content": "夜寝る前にちょうどいい一角獣（ユニコーン）が登場する物語を作ってください。"
        }
    ]
)

print(completion.choices[0].message.content)
