import requests
from time import sleep


def loader() -> None:  # Just for fun)
    print('Загрузка файла...')
    for i in range(1, 20):
        e = '=' * i
        u = ' ' * (20-i-1)
        print(f'[{e}{u}] {i*5+5}%', end='')
        sleep(0.1)
        print('\r', end='')
    print()


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-type': 'application/json',
            'Authorization': f'OAuth {self.token}',
        }

    def _get_upload_link(self, file_path: str) -> str:
        url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        upload_params = {'path': file_path, 'overwrite': 'true'}
        response = requests.get(url,
                                headers=self.get_headers(),
                                params=upload_params)
        try:
            upload_url = response.json()['href']
        except KeyError:
            if response.json()['message']:
                print('Ошибка:', response.json()['message'])
            return None
        return upload_url

    def upload(self, file_path: str) -> int:
        print('Получение ссылки для загрузки...')
        if self._get_upload_link(file_path):
            response = requests.put(self._get_upload_link(file_path),
                                    data=open(file_path, 'rb'))
            print('Ссылка успешно получена.')
            return response.status_code
        print('Ошибка получения ссылки.')
        return 0


if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = '1.txt'
    my_token = input('Введите Ваш токен:')
    uploader = YaUploader(my_token)
    result = uploader.upload(path_to_file)
    if result == 201:
        loader()
        print('Файл успешно загружен.')
