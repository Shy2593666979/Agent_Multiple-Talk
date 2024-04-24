# encoding=utf-8
import logging

from scene_config import scene_prompts
from scene_processor.scene_processor import SceneProcessor
from utils.helpers import get_raw_slot, update_slot, format_name_value_for_logging, is_slot_fully_filled, send_message, \
    extract_json_from_string, get_dynamic_example, clean_slot_json, clear_agent_json, update_agent_json
from utils.prompt_utils import get_slot_update_message, get_slot_query_user_message
from utils.function_api import Call_API
import agent

class CommonProcessor(SceneProcessor):
    def __init__(self, scene_config, slot, current_purpose):
        parameters = scene_config["parameters"]
        self.scene_config = scene_config
        self.scene_name = scene_config["name"]
        self.slot_template = get_raw_slot(parameters)
        self.slot_dynamic_example = get_dynamic_example(scene_config)
        self.current_purpose = current_purpose
        self.slot = slot
        self.scene_prompts = scene_prompts

    def process(self, user_input, history_content,chatId):
        # 处理用户输入，更新槽位，检查完整性，以及与用户交互
        # 先检查本次用户输入是否有信息补充，保存补充后的结果   编写程序进行字符串value值diff对比，判断是否有更新
        message = get_slot_update_message(self.scene_name, self.slot_dynamic_example,self.slot, user_input)  # 优化封装一下 .format  入参只要填input
        
        new_info_json_raw = send_message(message, user_input)
        
        current_values = extract_json_from_string(new_info_json_raw)
        logging.debug('current_values: %s', current_values)
        logging.debug('slot update before: %s', self.slot)

        update_slot(current_values, self.slot)
        update_agent_json(self.current_purpose, self.slot, chatId)

        logging.debug('slot update after: %s', self.slot)
        # 判断参数是否已经全部补全
        if is_slot_fully_filled(self.slot):
            # 参数补全的情况-----
            
            # 不需要用户二次确认
            if self.scene_name not in agent.is_user_comfirm:
                return Call_API(self.slot,self.scene_config,self.scene_name,user_input)
            
            # 需要用户二次确认
            if user_input == "YES":
                # 用户确认清空参数
                slot = self.slot

                self.slot = clean_slot_json(self.scene_config["parameters"])
                clear_agent_json(self.current_purpose,chatId)

                return Call_API(slot,self.scene_config,self.scene_name,"确认")
            else:
                self.respond_with_complete_data()

                prompt = f'''
                    # role：
                        你当前是一个客服，负责将这些参数返回给用户
                    # 已知信息：
                        这是{self.scene_name}场景下的参数数据：
                        {format_name_value_for_logging(self.slot)}
                    # 目标
                        你需要做的是将这些数据总结后交给用户
                    # 注意
                        1.说话要温柔一些，要有客服的风度。
                        2.不要有废话，让用户直接就能看到自己输入的数据是否有误。
                    ''' 
                return send_message(prompt,user_input) + "\n 如果您认为数据无误，请输出：确认"
        else:
            return self.ask_user_for_missing_data(user_input)


    def respond_with_complete_data(self):
        # 当所有数据都准备好后的响应
        logging.debug(f'%s ------ 参数已完整，详细参数如下', self.scene_name)
        logging.debug(format_name_value_for_logging(self.slot))
        logging.debug(f'正在请求%sAPI，请稍后……', self.scene_name)
        
        print(format_name_value_for_logging(self.slot) + '\n正在请求{}API，请稍后……'.format(self.scene_name))


    def ask_user_for_missing_data(self, user_input):
        message = get_slot_query_user_message(self.scene_name, self.slot, user_input)
        # 请求用户填写缺失的数据
        result = send_message(message, user_input)
        return result
