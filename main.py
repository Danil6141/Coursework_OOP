import json
import requests
import sys
import os
from dotenv import load_dotenv



# Курсовая работа "Ip Detector"
# В Интернете часто ходит шутка, что можно вычислить по IP.
# Давайте реализуем эту шутку.
#
# Цель:
# Разработать Python-программу, которая:#
# 1. определяет текущий IP-адрес пользователя;
# 2. получает географическую информацию по этому IP через внешний API;
# 3. сохраняет полученные данные в формате JSON;
# 4. загружает файл на Яндекс.Диск через REST API.
# Задание:
# 1. С помощью сервиса ipify мы можем получить наш ip адрес
# 2. Далее через сервис ipinfo по api можем получить город, где
# 3. находится этот ip адрес https://ipinfo.io/188.242.138.63/geo
# 4.Необходимо сохранить эту информацию в json файл и загрузить на
# Яндекс.Диск

# Информация по Яндекс Диску есть в Полигоне
# Важно: Токен Яндекс.Диска публиковать в github не нужно!

load_dotenv()

token_id = os.getenv('YANDEX_DISK_TOKEN')

class Ipify_API:
    def __init__(self):
        pass

    def ipify_request(self):
        response = requests.get('https://api.ipify.org/?format=json')
        return response.json()['ip']

    def ipinfo_request(self):
        ip = self.ipify_request()
        response = requests.get(f'https://ipinfo.io/{ip}/geo')
        data = response.json()
        with open("user.json", "w", encoding="utf-8") as file:
            json.dump(data, file)

class Yandex_API:

    URL = "https://cloud-api.yandex.net/v1/disk/resources"

    def __init__(self, token):
        self.token = token
        self.headers = {'Authorization': f'OAuth {self.token}'}


    def creating_folder(self):
        params = {'path': 'Ip_Detector'}
        response = requests.put(self.URL, params=params,
                                headers=self.headers)

    def uploading_file_to_disk(self):
        params = {'path': 'Ip_Detector/user.json'}
        response = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                params = params,
                                headers = self.headers)

        if response.status_code == 409:
            print('Папка уже создана')
            sys.exit(0)
        upload_link = response.json()["href"]
        with open('user.json', 'rb') as file:
            requests.put(upload_link, files={'file': file})
        if response.status_code == 200:
            print('Файл загружен на Яндекс Диск')
        os.remove('user.json')



if __name__ == '__main__':
    ipify_API = Ipify_API()
    ipify_API.ipinfo_request()
    yandex_API = Yandex_API(token_id)
    yandex_API.creating_folder()
    yandex_API.uploading_file_to_disk()

