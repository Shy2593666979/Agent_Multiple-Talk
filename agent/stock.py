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

def Call_Stock_API(market,stock_id,scene_name,user_input):
    if market == "A股" :
        headers ={"Content-Type": "application/x-www-form-urlencoded"}
        url = "http://web.juhe.cn/finance/stock/hs"
        params = {
            "key":config.stock_Key, # 在个人中心->我的数据,接口名称上方查看
            "gid":stock_id, # 股票编号，上海股市以sh开头，深圳股市以sz开头如：sh601009
        }
        resp = requests.get(url,params,headers=headers)
        data = json.loads(resp.text)
        
        if data["error_code"] == 0:
            # 自己提取json信息
            """
            name = data['result'][0]['data']['name']
            date = data['result'][0]['data']['name']
            increPer = data['result'][0]['data']['increPer'] # 涨跌幅百分比，负数表示下跌。
            increase = data['result'][0]['data']['increase'] # 涨跌额
            todayMax = data['result'][0]['data']['todayMax'] # 当日最大
            todayMin = data['result'][0]['data']['todayMin'] # 当日最低价
            todayStartPri = data['result'][0]['data']['todayStartPri'] # 当日开盘价
            traAmount = data['result'][0]['data']['traAmount'] # 当日累计成交金额
            traNumber = data['result'][0]['data']['traNumber'] # 当日累计成交量
            api_prompt = f'''A股中{name}{date}的股票信息如下: \n
                涨跌幅百分比：{increPer}\n
                涨跌额：{increase}\n
                当日最高价：{todayMax}\n
                当日最低价：{todayMin}\n
                当日开盘价：{todayStartPri}\n
                当日累计成交金额：{traAmount}\n
                当日累计成交量：{traNumber}
            '''
            """
            # json交给大模型去提取
            api_prompt = "以下是股票信息"
            data_list = data['result'][0]['data']
            for key, value in data_list.items():
                api_prompt += f"{key}:{value}\n"
            api_prompt += "根据这些信息总结交给用户，一定要准确和全面"

            prompt = slot_answer.format(scene_name,api_prompt,user_input)
            return send_message(prompt,user_input)
        else:
            prompt = slot_answer.format(scene_name,f"请检查您输入的股票编号{stock_id}在{market}中是否存在",user_input)
            return send_message(prompt,user_input)
    elif market == "港股":
        headers ={"Content-Type": "application/x-www-form-urlencoded"}
        url = "http://web.juhe.cn/finance/stock/hk"
        params = {
            "key":config["stock_Key"], # 在个人中心->我的数据,接口名称上方查看
            "num":stock_id, # 股票代码，如：00001 为“长江实业”股票代码
        }
        resp = requests.get(url,params,headers=headers)
        data = json.loads(resp.text)

        if data["error_code"] == 0:
            api_prompt = "以下是股票信息"
            data_list = data['result'][0]['data']
            for key, value in data_list.items():
                api_prompt += f"{key}:{value}\n"
            api_prompt += "根据这些信息总结交给用户，一定要准确和全面"

            prompt = slot_answer.format(scene_name,api_prompt,user_input)
            return send_message(prompt,user_input)
        else:
            prompt = slot_answer.format(scene_name,f"请检查您输入的股票编号{stock_id}在{market}中是否存在",user_input)
            return send_message(prompt,user_input)
    else:

        prompt = slot_answer.format(scene_name,f"请检查您选择的{market}股市是否存在，我只支持查询A股和港股",user_input)
        return send_message(prompt,user_input)