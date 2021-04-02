import queue
import os
import pytesseract
from PIL import Image
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
import path
from settings import config_parser
from classes.translate_provider import Translator
from classes.vk_parser import VKParser
from classes.image_processor import ImageSaver
from langdetect import detect
import serializers


SAVE_PATH = config_parser.SAVE_PATH
TOKEN = config_parser.VK_TOKEN
GROUP_ID = config_parser.GROUP_ID

IMAGES_QUEUE = queue.Queue()

session = vk_api.VkApi(token=TOKEN)
longpool =  VkBotLongPoll(vk=session, group_id=GROUP_ID, wait=1)
vk = session.get_api()

#Создаёт список для очереди
def make_queue_of_process_images(save_path):
    list_of_not_translated_images = os.listdir(save_path)
    return [path.Path('not_translated_images/' + i).abspath() for i in list_of_not_translated_images]

#Получает полный код языка
def get_lang_code(finded_code):
    data = serializers._data
    for i in data.result:
        if i['code_alpha_1'] == finded_code:
            return i['full_code']
            break

#Логика работы бота
for event in longpool.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        user_text = event.object["text"]
        user_id = event.object["from_id"]
        event_json = event.object
        if user_text == '-языки':
            vk.messages.send(
                user_id=user_id,
                random_id=get_random_id(),
                message = 'ru_RU - Русский\nen_GB - Английский'
            )
            continue
        image_url = VKParser.get_image_url(event.object)
        ImageSaver.save_image_to_path(SAVE_PATH, image_url, user_id)

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
            lang = detect(result)
            from_lang = get_lang_code(lang)
            try: 
                response = Translator.translate(from_lang, user_text, result)
                vk.messages.send(user_id=user_id,
                                 random_id=get_random_id(),
                                 message=response)
            except vk_api.exceptions.ApiError:
                vk.messages.send(user_id=user_id,
                                 random_id=get_random_id(),
                                 message='Не могу обработать фото')
            finally:
                os.remove(image_to_process)
        print('FUCK')
