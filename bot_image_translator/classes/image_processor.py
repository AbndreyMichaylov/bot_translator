import requests
import json

class ImageSaver:
    def create_user_json(save_path, user_id, file_name):
        json_file_name = str(user_id) + '.json'
        with open(save_path + json_file_name, 'w') as j:
            saved_json = ({
                "image": file_name,
                "user": user_id
            })
            json.dump(saved_json, j)


# Сохраняет изображение по урлу в папку по указанному пути

    def save_image_to_path(save_path, img_url, user_id):
        image = requests.get(img_url)
        file_name = str(user_id) + '.jpg'
        with open(save_path + file_name, 'wb') as f:
            f.write(image.content)
        ImageSaver.create_user_json('users_data/', user_id, file_name)
