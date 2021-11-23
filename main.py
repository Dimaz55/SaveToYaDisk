import requests
from time import sleep


def loader():
    print('Загрузка...')
    for i in range(1, 20):
        e = '=' * i
        u = ' ' * (20-i-1)
        print(f'[{e}{u}]', end='')
        sleep(0.1)
        print('\r', end='')
    print()
    return None

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-type': 'application/json',
            'Authorization': f'OAuth {self.token}',
        }

    def _get_upload_link(self, file_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        self.path = file_path
        prms = {'path': self.path, 'overwrite': 'true'}
        response = requests.get(url, headers=self.get_headers(), params=prms)
        try:
            url_to_upload = response.json()['href']
        except KeyError:
            print('Ошибка:', response.json()['message'])
            return None

        return url_to_upload

    def upload(self, file_path: str):
        print('Получение ссылки для загрузки...')
        if self._get_upload_link(file_path):
            response = requests.put(self._get_upload_link(file_path), data=open(file_path, 'rb'))
            print('Ссылка успешно получена.')
            return response.status_code
        print('Ошибка получения ссылки.')
        return 0


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = '1.txt'
    with open('token.txt') as f:
        my_token = f.readline().strip()
    uploader = YaUploader(my_token)
    result = uploader.upload(path_to_file)
    if result == 201:
        loader()
        print('Успешно загружено')
