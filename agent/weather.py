import config
import requests
from utils.helpers import send_message

import scene_config.scene_prompts
slot_answer = scene_config.scene_prompts.slot_api_answer


# 查询天气信息的API
def Call_Weather_API(location,scene_name,user_input):
    params_realtime = {
        'key': config.Weather_Key,
        'city': location,
        'extensions': 'all'
    }

    res = requests.get(url=config.Weather_Url, params=params_realtime)

    weather = res.json()

    if weather["count"] == "0":
        weather_prompt = f"获取{location}地区的实时天气失败，请检查是否存在该地区"
        prompt = slot_answer.format(scene_name,weather_prompt,user_input)
        model_answer = send_message(prompt,user_input)
        return  model_answer
    
    report_time = weather.get('forecasts')[0].get("reporttime")  # 获取发布数据时间
    date = weather.get('forecasts')[0].get("casts")[0].get('date')  # 获取日期
    day_weather = weather.get('forecasts')[0].get("casts")[0].get('dayweather')  # 白天天气现象
    night_weather = weather.get('forecasts')[0].get("casts")[0].get('nightweather')  # 晚上天气现象
    day_temp = weather.get('forecasts')[0].get("casts")[0].get('daytemp')  # 白天温度
    night_temp = weather.get('forecasts')[0].get("casts")[0].get('nighttemp')  # 晚上温度
    day_wind = weather.get('forecasts')[0].get("casts")[0].get('daywind')  # 白天风向
    night_wind = weather.get('forecasts')[0].get("casts")[0].get('nightwind')  # 晚上风向
    day_power = weather.get('forecasts')[0].get("casts")[0].get('daypower')  # 白天风力
    night_power = weather.get('forecasts')[0].get("casts")[0].get('nightpower')  # 晚上风力


    weather_prompt = f"地点是{location}" + f"发布数据的时间{report_time}" + f"现在的日期是{date}" + f"白天天气现象{day_weather}" + f"晚上天气现象{night_weather}" + f"白天温度{day_temp}" + f"晚上温度{night_temp}" + f"白天风向{day_wind}" + f"晚上风向{night_wind}" + f"白天风力{day_power}" + f"晚上风力{night_power}"

    prompt = slot_answer.format(scene_name,weather_prompt,user_input)
    model_answer = send_message(prompt,user_input)

    return  model_answer