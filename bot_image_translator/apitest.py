import requests
import json  

r = requests.post('https://api-b2b.backenster.com/b1/api/v3/translate', 
                headers={"Authorization" : "a_gOZD4Z1urbiAvgfPjuCIzMOArpW35p6MPg2Wz49qktE7QvqiH7loxIRs92RTWDzBFozmGgxBu16BBZE6",
                         "accept":"application/json",
                         "Content-Type":"application/json"},
                data = json.dumps({"from": "en_GB",
                        "to": "ru_RU",
                        "data": "London is the capital and largest city of England and of the United Kingdom.",
                        "platform": "api"}))
r2 = requests.get('https://api-b2b.backenster.com/b1/api/v3/getLanguages?platform=api&code=en_GB', 
                headers={"Authorization" : "a_gOZD4Z1urbiAvgfPjuCIzMOArpW35p6MPg2Wz49qktE7QvqiH7loxIRs92RTWDzBFozmGgxBu16BBZE6",
                         "accept":"application/json"})
print(r2.json())