import os
import vk_api
import requests
import datetime
from tqdm import tqdm

class VkRequest:
    def __init__(self, tokenVK: str , user_id, screen_name: str, version='5.131'):
        """Метод для получения начальных(основных) параметров запроса для VK
        """
        self.token = tokenVK
        self.id = user_id
        self.name = screen_name
        self.version = version
        self.start_params = {'access_token': self.token, 'v': self.version}
        self.json, self.export_dict = self._sort_info()

    def _get_photo_info(self):
        """Метод для получения количества фотографий и массива фотографий"""
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'extended': 1,
                  'rev': 1
                  }
        photo_info = requests.get(url, params={**self.start_params, **params}).json()['response']
        return photo_info['count'], photo_info['items']


    def _resolve_name(self, tokenVK):
        vk = vk_api.VkApi(token = tokenVK)
        id_ = vk.method('users.get', {'self.id': 'self.name'})[0]['id']
        return id_

    def _find_max_dpi(self, dict_in_search):
        """Функция возвращает ссылку на фото максимального размера и размер фото"""
        max_dpi = 0
        need_elem = 0
        for j in range(len(dict_in_search)):
            file_dpi = dict_in_search[j].get('width') * dict_in_search[j].get('height')
            if file_dpi > max_dpi:
                max_dpi = file_dpi
                need_elem = j
        return dict_in_search[need_elem].get('url'), dict_in_search[need_elem].get('type')

    def _time_convert(self, time_unix):
        """Функция преобразует дату загрузки фото в привычный формат"""
        time_bc = datetime.datetime.fromtimestamp(time_unix)
        str_time = time_bc.strftime('%Y-%m-%d time %H-%M-%S')
        return str_time

    def _get_logs_only(self):
        """Метод для получения словаря с параметрами фотографий"""
        photo_count, photo_items = self._get_photo_info()
        result = {}
        for i in range(photo_count):
            likes_count = photo_items[i]['likes']['count']
            url_download, picture_size = self._find_max_dpi(photo_items[i]['sizes'])
            time_warp = self._time_convert(photo_items[i]['date'])
            new_value = result.get(likes_count, [])
            new_value.append({'likes_count': likes_count,
                              'add_name': time_warp,
                              'url_picture': url_download,
                              'size': picture_size})
            result[likes_count] = new_value
        return result

    def _sort_info(self):
        """Метод для получения словаря с параметрами фотографий и списка JSON для выгрузки"""
        json_list = []
        sorted_dict = {}
        picture_dict = self._get_logs_only()
        counter = 0
        for elem in picture_dict.keys():
            for value in picture_dict[elem]:
                if len(picture_dict[elem]) == 1:
                    file_name = f'{value["likes_count"]}.jpeg'
                else:
                    file_name = f'{value["likes_count"]} {value["add_name"]}.jpeg'
                json_list.append({'file name': file_name, 'size': value["size"]})
                if value["likes_count"] == 0:
                    sorted_dict[file_name] = picture_dict[elem][counter]['url_picture']
                    counter += 1
                else:
                    sorted_dict[file_name] = picture_dict[elem][0]['url_picture']
        return json_list, sorted_dict