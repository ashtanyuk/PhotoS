# 
# PhotoS
# ------
# загрузка фотоальбомов с ВК
# 
# 

import vk_api
import random
import time
import requests
import os

# Авторизация в VK API
vk_session = vk_api.VkApi(token='...') # access_token
vk = vk_session.get_api()

# ID сообществ, из которых берем фотографии 
source_group_id = 2515255

# получение списка альбомов целевого сообщества
albums = vk.photos.getAlbums(owner_id=-source_group_id)['items']
print("Число альбомов: " + str(len(albums)))

for album in albums:
    
    album_id = album['id']
    album_title = album['title']

    print("Название альбома: " + album_title)
    
    # получение списка фотографий из альбома источника
    photos = vk.photos.get(owner_id=-source_group_id, album_id=album_id, count=1000)['items']
    print("Число фотографий: " + str(len(photos)))

    if not os.path.exists("images/" + album_title):
        os.makedirs("images/" + album_title)
    else:
        continue # за обрабатываем уже загруженное

    fotos = []
    for photo in photos:
        ph_numbers = len(photo["sizes"])
        if ph_numbers > 1:
           file_url = photo["sizes"][-1]["url"]
        else:
           print(photo["sizes"])

        filename = file_url.split("/")[-1].split("?")[0]
        print(filename)
        fotos.append(filename)
        time.sleep(0.2)
        api = requests.get(file_url)

        with open("images/" + album_title + "/" +filename, "wb") as file:
            file.write(api.content)
