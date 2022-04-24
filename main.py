import os
import requests
import datetime
from tqdm import tqdm
import classVK
import classYandex


tokenVK = input('Введите токен из Вконтакте: ')
tokenYandex = input('Введите токен с Полигона Яндекс.Диска: ')
user_id = classVK.VkRequest._resolve_name(input('Введите идентификатор пользователя VK: '),tokenVK)
num = int(input('Введите количество загружаемых фото: '))
folder_name = str(input('Введите имя файла: '))

if __name__ == "__main__":
    my_VK = classVK.VkRequest(tokenVK, user_id, screen_name=user_id)
    print(my_VK.json)

    my_yandex = classYandex.Yandex(folder_name, tokenYandex, num)
    my_yandex.create_copy(my_VK.export_dict)
