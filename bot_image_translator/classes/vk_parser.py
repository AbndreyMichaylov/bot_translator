from .serializers.serializers import VkUserRequestSerializer
from .exceptions.no_photos import NoPhotosException
import json

class VKParser:
    #Недоработанная функция рекурсивного поиска изображений в пересланных сообщениях
    def get_attachment_url(fwd_message):
        try:
            attach = fwd_message["fwd_messages"][0]
            return VKParser.get_attachment_url(attach)
        except KeyError or TypeError or IndexError:
            return [p["photo"]["sizes"][-1]["url"] for p in fwd_message["attachments"]]

    def get_image_url(event_object):
        data = VkUserRequestSerializer.parse_raw(json.dumps(event_object))
        images_urls = [a.photo.sizes[-1].url for a in data.attachments]
        if len(images_urls) == 0:
            raise NoPhotosException
        return images_urls
