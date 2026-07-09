import requests

def get_image():
    response = requests.get(f'https://dog.ceo/api/breeds/image/random')
    print(response)
    print(response.json())


if __name__ == "__main__":
    get_image()