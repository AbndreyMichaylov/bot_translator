

class VKParser:
    # Рекурсивно находит ссылку среди пересланных сообщений

    def get_attachment_url(fwd_message):
        try:
            attach = fwd_message["fwd_messages"][0]
            return VKParser.get_attachment_url(attach)
        except KeyError or TypeError or IndexError:
            return [p["photo"]["sizes"][-1]["url"] for p in fwd_message["attachments"]]

# Парсит пришедший json от вк

    def get_image_url(event_object):
        try:
            print(event_object.count('attachments'))
            exit()
            images_urls = [p["photo"]["sizes"][-1]["url"] for p in event_object["attachments"]]
            return images_urls
        except:
            images_urls = VKParser.get_attachment_url(event_object)
            return images_urls
