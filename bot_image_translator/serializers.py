from pydantic import BaseModel
import json

class Codes(BaseModel):
    full_code : str
    code_alpha_1 : str

class LangSerializer(BaseModel):
    result = [Codes]

_data : LangSerializer

with open('languages.json', 'r') as langs:
    data = LangSerializer.parse_raw(langs.read())
    _data = data
