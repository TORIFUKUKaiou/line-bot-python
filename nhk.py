import requests

def get_items(query):
    response = requests.get(f'https://api.nhk.or.jp/v2/pg/list/130/g1/2023-06-14.json?key=key')
    print(response)
    print(response.json())


if __name__ == "__main__":
    get_items('Python')