import requests
import json
import uuid

class ImageSaver:

    # Сохраняет изображения по урлу в папку по указанному пути
    def save_image_to_path(save_path, imgs_urls):
        for i in imgs_urls:
            image = requests.get(i)
            file_name = str(uuid.uuid4()) + '.jpg'
            with open(save_path + file_name, 'wb') as f:
                f.write(image.content)
