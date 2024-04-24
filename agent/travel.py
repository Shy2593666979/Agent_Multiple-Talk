import config
import requests
from utils.helpers import send_message
import urllib
from utils.data_format_utils import clean_content
import scene_config.scene_prompts
slot_answer = scene_config.scene_prompts.slot_api_answer


# 查询景区的信息API
def Call_Travel_API(travel_name,scene_name,user_input):

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {
    'key': config.Travel_Key,
    'word': travel_name,
    'num': 1,  # 返回数量，根据需求填写
    }
    response = requests.get(url=config.Travel_Url,headers=headers,params=params)

    if response.status_code == 200:
        data = response.json()
        if data["error_code"] == 0:
            content = data["result"]["list"][0]["content"]

            prompt = slot_answer.format(scene_name,content,user_input)

            return send_message(prompt,user_input)
        else:
            prompt = slot_answer.format(scene_name,"没有找到这个景区",user_input)

            return send_message(prompt,user_input)