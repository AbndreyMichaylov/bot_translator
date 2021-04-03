from .serializers.serializers import LangSerializer

class Langs:
    serializer = LangSerializer

    def get_langs():
        with open('languages.json', 'r') as langs:
            data = LangSerializer.parse_raw(langs.read())
            return data