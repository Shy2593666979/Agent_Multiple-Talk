import config
import requests
from utils.helpers import send_message
import urllib
from urllib.parse import quote
import json
import ssl
from utils.data_format_utils import clean_content
import scene_config.scene_prompts

slot_answer = scene_config.scene_prompts.slot_api_answer


def Call_News_API(name,scene_name,user_input):
    
    host = 'https://jisunews.market.alicloudapi.com'
    path = '/news/search'
    method = 'ANY'
    appcode = config.News_Key
    querys = f'keyword={quote(name)}'
    bodys = {"keyword": name}
    url = host + path + '?' + querys

    post_data = json.dumps(bodys)
    request = urllib.request.Request(url, post_data.encode('utf-8'))
    request.add_header('Authorization', 'APPCODE ' + appcode)
    # 根据API的要求，定义相对应的Content-Type
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(request, context=ctx)
    content = response.read().decode('utf-8')
    data = json.loads(content)

    # 访问 "list" 数组
    if data["status"] != 0:
        prompt = slot_answer.format(scene_name,f"未找到与{name}相关的新闻信息",user_input)
        return send_message(prompt,user_input)
    else:
        list_items = data["result"]["list"]
        api_prompt = ""
        # 最多取5数据
        News_number = 5

        for item in list_items:
            content = item["content"]
            time = item["time"]
            src = item["src"]
            cleaned_content = clean_content(content)
            api_prompt += f"时间：{time},新闻信息:{cleaned_content}，新闻来源：{src}\n"

            print(api_prompt)

            if News_number <= 0:
                break
            News_number -= 1

        # 加载到当前环境
        prompt = slot_answer.format(scene_name,api_prompt,user_input) + "每个新闻都必须带上具体的时间"

        return send_message(prompt,user_input)