import config
import requests
from utils.helpers import send_message
import urllib
import json,ssl
from utils.data_format_utils import clean_content
import scene_config.scene_prompts
slot_answer = scene_config.scene_prompts.slot_api_answer

def Call_Exchange_API(money_name,scene_name,user_input):
    with open('/home/z00013696/lyq-file/Script/function/utils/exchange.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
 
    # 创建一个字典来存储 "com" 和 "no" 值
    result_dict = {}
    
    print(data)

    for item in data['result']['list']:
        name_value = item.get("name")
        code_value = item.get("code")
        # 将 "com" 和 "no" 值存储到字典中
        result_dict[name_value] = code_value
    
    if result_dict.get(money_name) is None:
        prompt = slot_answer.format(scene_name,f"请检查您选择的货币{money_name}是否正确",user_input)
        return send_message(prompt,user_input)
    
    host = 'https://jisuhuilv.market.alicloudapi.com'
    path = '/exchange/single'
    method = 'GET'
    appcode = config.News_Key
    querys = f'currency={result_dict.get(money_name)}'
    bodys = {"currency": money_name}
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

    if data["status"] != 0:
        prompt = slot_answer.format(scene_name,f"请检查您选择的货币{money_name}是否正确",user_input)
        return send_message(prompt,user_input)
    else:
        api_prompt = f"{money_name}的汇率信息如下："
        currency_list = data["result"]["list"]

        # 遍历并打印出每个货币的名称和汇率
        rate_count = 10

        for currency, info in currency_list.items():
            name = info["name"]
            rate = info["rate"]
            updatetime = info["updatetime"]
            api_prompt += f"货币名称: {name}, 汇率: {rate}, 更新时间: {updatetime}"

            rate_count = rate_count - 1

            if rate_count <= 0:
                break
        prompt = slot_answer.format(scene_name,api_prompt,user_input)
        return send_message(prompt,user_input)