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

def Call_Oil_API(province,scene_name,user_input):

    province = province.replace("省","")
    province = province.replace("市","")

    encoded_province = urllib.parse.quote(province.encode('utf-8'))
    host = 'https://youjia.market.alicloudapi.com'
    path = '/lundroid/youjia'
    method = 'ANY'
    appcode = config.News_Key
    querys = f'province={encoded_province}'
    bodys = {"province": province}
    url = host + path + '?' + querys

    post_data = json.dumps(bodys)
    request = urllib.request.Request(url) #, post_data.encode('utf-8'))
    request.add_header('Authorization', 'APPCODE ' + appcode)
    # 根据API的要求，定义相对应的Content-Type
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(request, context=ctx)
    content = response.read().decode('utf-8')
    data = json.loads(content)

    # print(data) #-------------------------------------------------

    if data["resp"]["RespCode"] == 200:
        list_data = data["data"]
        api_prompt = f'今天{province}地区的油价如下：柴油：{list_data[0]["type0"]}/升,92号汽油：{list_data[0]["type92"]}/升,95号汽油：{list_data[0]["type95"]}/升,98号汽油：{list_data[0]["type98"]}/升,最新一次更新时间是{list_data[0]["updateTime"]}'
        prompt = slot_answer.format(scene_name,api_prompt,user_input)

        return send_message(prompt,user_input)
    else:
        prompt = slot_answer.format(scene_name,f"请检查你输入的{province}地区是否正确",user_input)

        return send_message(prompt,user_input)