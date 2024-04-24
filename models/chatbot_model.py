# encoding=utf-8
import logging

from scene_processor.impl.common_processor import CommonProcessor
from utils.data_format_utils import extract_continuous_digits, extract_float
from utils.helpers import send_message, get_raw_slot, get_agent_current_scene, update_agent_current_scene


class ChatbotModel:
    def __init__(self, scene_templates: dict):
        self.scene_templates: dict = scene_templates
        self.current_purpose: str = ''
        self.processors = {}
        self.scene_slot = {}
        for key in self.scene_templates:
            scene_config = self.scene_templates.get(key)
            parameters = scene_config["parameters"]
            self.scene_slot[key] = get_raw_slot(parameters)


    @staticmethod
    def load_scene_processor(self, scene_config,slot, current_purpose):
        try:
            return CommonProcessor(scene_config,slot,current_purpose)
        except (ImportError, AttributeError, KeyError):
            raise ImportError(f"未找到场景处理器 scene_config: {scene_config}")

    def is_related_to_last_intent(self, user_input,history):
        RELATED_INTENT_THRESHOLD = 0.7
        
        """
        判断当前输入是否与上一次意图场景相关
        """
        if not self.current_purpose:
            return False
        prompt = f'''
        # 目标：
            你需要判断当前用户输入内容与当前对话场景的关联性:
            当前对话场景: {self.scene_templates[self.current_purpose]['description']}
            当前用户输入: {user_input}
            历史对话： role：AI ， content:{history}
        # 举例：
            当前对话场景：请假申请
            当前用户输入：好的，谢谢
            输出：0.1

            当前对话场景：请假申请
            当前用户输入：田明广
            输出：0.7

            当前对话场景：请假申请
            当前用户搜索：我想要办理套餐
            输出：0.0

            当前对话场景：请假申请
            当前用户搜索：我不申请了
            输出：0.0

            
        # 注意：
            这两次输入是否关联（仅用小数回答关联度，得分范围0.0至1.0）'''
        result = send_message(prompt, None)
        return extract_float(result) >= RELATED_INTENT_THRESHOLD

    def recognize_intent(self, user_input, chatId):
        # 根据场景模板生成选项
        purpose_options = {}
        purpose_description = {}
        index = 1
        for template_key, template_info in self.scene_templates.items():
            purpose_options[str(index)] = template_key
            purpose_description[str(index)] = template_info["description"]
            index += 1
        options_prompt = "\n".join([f"{key}. {value} - 请回复{key}" for key, value in purpose_description.items()])
        options_prompt += "\n0. 闲聊场景，例如：你好？你是谁？ - 请回复0"

        # 发送选项给用户
        user_option = f"有下面多种场景，需要你根据用户输入进行判断，时间的问题应该选择请假申请的序号。只答选项\n{options_prompt}\n用户输入：{user_input}\n请回复序号："
        user_choice = send_message(user_option, user_input)

        logging.debug(f'purpose_options: %s', purpose_options)
        logging.debug(f'user_choice: %s', user_choice)

        user_choices = extract_continuous_digits(user_choice)

        # 根据用户选择获取对应场景
        if user_choices and user_choices[0] != '0':
            self.current_purpose = purpose_options[user_choices[0]]
            update_agent_current_scene(self.current_purpose,chatId)
        if self.current_purpose:
            print(f"用户选择了场景：{self.scene_templates[self.current_purpose]['name']}")
            # 这里可以继续处理其他逻辑
        else:
            update_agent_current_scene('',chatId)
            # 用户输入的选项无效的情况，可以进行相应的处理
            print("无效的选项，请重新选择")

    def get_processor_for_scene(self, scene_name):
        if scene_name in self.processors:
            return self.processors[scene_name]

        scene_config = self.scene_templates.get(scene_name)
        if not scene_config:
            raise ValueError(f"未找到名为{scene_name}的场景配置")

        processor_class = self.load_scene_processor(self, scene_config,self.scene_slot[scene_name],self.current_purpose)
        self.processors[scene_name] = processor_class
        return self.processors[scene_name]

    def process_multi_question(self, user_input,history_content,chatId):
        """
        处理多轮问答
        :param user_input:
        :return:
        """
        self.current_purpose =  get_agent_current_scene(chatId)
        # 查看当前场景参数是否词槽填满且用户确认
        if "确认" in user_input:
            self.get_processor_for_scene(self.current_purpose)

            update_agent_current_scene('',chatId)

            current_purpose = self.current_purpose
            self.current_purpose = ''
            return self.processors[current_purpose].process("YES", None,chatId)

        # 检查当前输入是否与上一次的意图场景相关
        if self.is_related_to_last_intent(user_input,history_content):
            pass
        else:
            # 不相关时，重新识别意图
            self.current_purpose = ''
            self.recognize_intent(user_input,chatId)
        logging.info('current_purpose: %s', self.current_purpose)

        if self.current_purpose in self.scene_templates:
            # 根据场景模板调用相应场景的处理逻辑
            self.get_processor_for_scene(self.current_purpose)
            # 调用抽象类process方法
            return self.processors[self.current_purpose].process(user_input,None,chatId)
        
        print("未命中已有的场景，直接交给大模型自行回答---------------\n")
        return user_input


