from utils.helpers import send_message
import requests
import scene_config.scene_prompts
from utils.data_format_utils import clean_content
import json
import re
import urllib.request
import urllib,sys
import ssl,os
from utils.environ import set_proxy_environ
from urllib.parse import quote
import config

from agent.exchange_rate import Call_Exchange_API
from agent.news import Call_News_API
from agent.oil_price import Call_Oil_API
from agent.stock import Call_Stock_API
from agent.travel import Call_Travel_API
from agent.weather import Call_Weather_API
from agent.google_search import Call_Google_API
from agent.apply_for_package import apply_for_package_API
from agent.apply_leave import Call_leave_API

slot_answer = scene_config.scene_prompts.slot_api_answer


def Call_API(slot,scene_config,scene_name,user_input):
    # 设置代理
    set_proxy_environ()

    if  scene_config["name"] == "问天气" :
        print("weather_query--------------------------===================\n")
        return Call_Weather_API(slot[0]["value"],scene_name,user_input)
    elif scene_config["name"] == "查景区" :
        print("travel_query--------------------------===================\n")
        return Call_Travel_API(slot[0]["value"],scene_name,user_input)
    elif scene_config["name"] == "查新闻":
        print("查新闻--------------------------===================\n")
        return Call_News_API(slot[0]["value"],scene_name,user_input)
    elif scene_config["name"] == "查油价":
        print("查油价--------------------------===================\n")
        return Call_Oil_API(slot[0]["value"],scene_name,user_input)
    elif scene_config["name"] == "查股票":
        print("查股票--------------------------===================\n")
        return Call_Stock_API(slot[0]["value"],slot[1]["value"],scene_name,user_input)
    elif scene_config["name"] == "查汇率":
        print("查汇率--------------------------===================\n")
        return Call_Exchange_API(slot[0]["value"],scene_name,user_input)
    elif scene_config["name"] == "google搜索":
        print("google搜索--------------------------===================\n")
        return Call_Google_API(scene_name,user_input)
    elif scene_config["name"] == "请假申请":
        print("请假申请--------------------------===================\n")
        return Call_leave_API(slot,scene_name,user_input)
    elif scene_config["name"] == "办理套餐":
        print("办理套餐--------------------------===================\n")
        return apply_for_package_API(slot,scene_name,user_input)
    else:
      print("-----------------------没调用API，直接交给大模型进行回答========================\n")













    

