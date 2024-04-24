import json
from utils.helpers import send_message
from langchain.utilities import SerpAPIWrapper
from utils.environ import set_Google_environ,set_proxy_environ
import config
import requests
from scene_config.scene_prompts import google_message,google_prompt
from utils.date_utils import get_current_date


'''
def Call_Google_API(question,scene_name,user_input):
    set_Google_environ()

    search = SerpAPIWrapper()

    result = search.run(user_input)

    slot_answer = """
    # role：
        你现在是一个总结机器人。
    # 搜索出的信息：
        {}
    # 用户问题：
        用户输入:{}
    # 目标
        请你根据搜索出的信息和用户问题回复给用户
        注意每条数据需要分行"""
    prompt = slot_answer.format(result,user_input)

    return send_message(prompt,user_input)
'''
def Call_Google_API(scene_name,user_input):

    prompt = google_prompt.format(get_current_date(),user_input)

    new_question = send_message(prompt,user_input)

    google_url = "https://www.googleapis.com/customsearch/v1?key={}&q={}&cx={}&lr=lang_zh-CN&num=5&sort=date&cr=countryCN"

    set_proxy_environ()
    
    data = requests.get(google_url.format(config.google_key_plus,new_question,config.google_engines_key)).text

    json_data = json.loads(data)

    # 提取item中的snippet字段的值
    snippet_values = [item.get('snippet', '') for item in json_data.get('items', [])]

    second_prompt = ""

    for snippet_value in snippet_values:
        second_prompt += snippet_value + "\n"
    
    final_prompt = google_message.format(get_current_date(),second_prompt,user_input)

    return send_message(final_prompt,user_input)
