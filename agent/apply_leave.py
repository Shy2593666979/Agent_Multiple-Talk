

def Call_leave_API(slot,scene_name,user_input):
    message = f'尊敬的XXX先生，您好！您的请假信息如下：\n主管：{slot[0]["value"]}\n申请理由：{slot[1]["value"]}\n请假类别：{slot[2]["value"]}\n开始日期：{slot[3]["value"]}\n结束日期：{slot[4]["value"]}'
    message += "\n您的请假信息申请成功，等待主管审批中~"
    return message
    
