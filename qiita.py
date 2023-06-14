import requests

def get_items(query):
    response = requests.get(f'https://qiita.com/api/v2/items?query={query}')
    print(response)
    # print(response.json())
    json = response.json()

    for title in map(lambda x: x['title'], json):
        print(title)


if __name__ == "__main__":
    get_items('Python')