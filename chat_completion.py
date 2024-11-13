import requests
import pprint

YOUR_API_KEY = 'YOUR_API_KEY'

def call(query_msg):
    url = "https://api.kyutech-arise.dev.haw.biz/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {YOUR_API_KEY}"
    }
    data = {
        "messages": [
            {
                "content": query_msg
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        json = response.json()
        pprint.pprint(json)

        return json["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}"

if __name__ == "__main__":
    reply = call('はげましてください！')
    print(reply)