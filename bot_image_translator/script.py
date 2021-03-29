import queue
import os
import pytesseract
from PIL import Image
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import requests
import uuid
import path
import requests
import json
import config_parser
from translate_provider import Translator
from langdetect import detect



SAVE_PATH = config_parser.SAVE_PATH
TOKEN = config_parser.VK_TOKEN
GROUP_ID = config_parser.GROUP_ID

IMAGES_QUEUE = queue.Queue()

session = vk_api.VkApi(token=TOKEN)
longpool =  VkBotLongPoll(vk=session, group_id=GROUP_ID, wait=1)
vk = session.get_api()

#Парсит пришедший json
def get_image_url(event_object):
    return event.object["attachments"][0]["photo"]["sizes"][-1]["url"]

#Сохраняет изображение по урлу в папку по указанному пути
def save_image_to_path(save_path, img_url):
    image = requests.get(img_url)
    random_name = str(uuid.uuid4()) + '.jpg'
    with open(save_path + random_name , 'wb') as f:
        f.write(image.content)

#Создаёт список для очереди
def make_queue_of_process_images(save_path):
    list_of_not_translated_images = os.listdir(save_path)
    return [path.Path('not_translated_images/' + i).abspath() for i in list_of_not_translated_images]


#Логика работы бота
for event in longpool.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        if event.object["text"] == '-языки':
            vk.messages.send(
                user_id=event.object["from_id"],
                random_id=get_random_id(),
                message = 'ru_RU - Русский\nen_GB - Английский'
            )
            continue
        image_url = get_image_url(event)

        save_image_to_path(SAVE_PATH, image_url)

        list_of_not_translated_images = os.listdir(SAVE_PATH)

        list_of_full_paths_of_files = make_queue_of_process_images(SAVE_PATH)

        #print(list_of_full_paths_of_files)
        #Заполняет очередь обработки изображений
        for image in list_of_full_paths_of_files:
            IMAGES_QUEUE.put(image)

        while not IMAGES_QUEUE.empty():
            image_to_process = IMAGES_QUEUE.get()

            img = Image.open(image_to_process)

            result = pytesseract.image_to_string(img, lang='ru+eng')
            print(result)
            lang = detect(result) + '_GB'
            print(lang)
            print(event.object['text'])
            #exit()
            try: 
                response = Translator.translate(lang, event.object['text'], result)
                vk.messages.send(user_id=event.object["from_id"],
                                 random_id=get_random_id(),
                                 message=response)
            except vk_api.exceptions.ApiError:
                vk.messages.send(user_id=event.object["from_id"],
                                 random_id=get_random_id(),
                                 message='Не могу обработать фото')
            finally:
                os.remove(image_to_process)
        print('FUCK')
