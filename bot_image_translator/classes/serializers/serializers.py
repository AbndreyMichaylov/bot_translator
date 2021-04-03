from pydantic import BaseModel
from typing import List, Dict


class _Codes(BaseModel):
    full_code : str
    code_alpha_1 : str

class LangSerializer(BaseModel):
    result : List[_Codes]

class _Urls(BaseModel):
    url : str

class _Sizes(BaseModel):
    sizes : List[_Urls]

class _Photos(BaseModel):
    photo : _Sizes

class VkUserRequestSerializer(BaseModel):
    from_id : int
    attachments : List[_Photos]