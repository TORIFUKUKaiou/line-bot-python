import requests

def get_program_list(key):
    response = requests.get(f'https://api.nhk.or.jp/v2/pg/list/130/g1/2025-04-20.json?key={key}')
    print(response)
    print(response.json())


if __name__ == "__main__":
    get_program_list('Your API Key')