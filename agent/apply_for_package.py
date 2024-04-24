from utils.helpers import send_message,format_name_value_for_logging

def apply_for_package_API(slot,scene_name,user_input):
    return f'尊敬的{slot[0]["value"]}先生，您好！感谢您选择我们的服务\n' + f'您的手机号：{slot[1]["value"]}的{slot[3]["value"]}办理成功！\n稍后会给您发送短信，请注意查收。请问还有什么需要我帮助的吗？'