

class VKParser:
    # Рекурсивно находит ссылку среди пересланных сообщений

    def get_attachment_url(fwd_message):
        try:
            attach = fwd_message["fwd_messages"][0]
            return VKParser.get_attachment_url(attach)
        except KeyError or TypeError or IndexError:
            return fwd_message["attachments"][0]["photo"]["sizes"][-1]["url"]

# Парсит пришедший json от вк

    def get_image_url(event_object):
        image_url = ''
        try:
            image_url = event_object["attachments"][0]["photo"]["sizes"][-1]["url"]
        except:
            image_url = VKParser.get_attachment_url(event_object)
        return image_url
