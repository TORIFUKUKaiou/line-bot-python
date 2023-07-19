import requests
import pprint

def call(query_msg):
    files = {
        'apikey': (None, 'YOUR_API_KEY'),
        'query': (None, query_msg.encode('utf-8')),
    }
    response = requests.post('https://api.a3rt.recruit.co.jp/talk/v1/smalltalk', files=files)
    json = response.json()
    pprint.pprint(json)

    reply = json['results'][0]['reply']
    print(reply)

    return reply

if __name__ == "__main__":
    call('好きな食べ物は何ですか')