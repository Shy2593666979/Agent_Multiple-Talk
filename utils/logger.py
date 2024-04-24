import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

cur_path = os.path.dirname(os.path.realpath(__file__))  # 当前项目路径
log_path = os.path.join(cur_path, '../logs')  # log_path为存放日志的路径
if not os.path.exists(log_path): os.mkdir(log_path)  # 若不存在logs文件夹，则自动创建

default_formats = {
    'log_format': '%(asctime)s-%(name)s-%(levelname)s: %(message)s'
}


class HandleLog:
    """
    先创建日志记录器（logging.getLogger），然后再设置日志级别（logger.setLevel），
    接着再创建日志文件，也就是日志保存的地方（logging.FileHandler），然后再设置日志格式（logging.Formatter），
    最后再将日志处理程序记录到记录器（addHandler）
    """

    def __init__(self, log_name):
        self.__now_time = datetime.now().strftime('%Y%m%d_%H%M%S')  # 当前日期格式化
        self.__all_log_path = os.path.join(log_path, log_name + "_all_" + self.__now_time + ".log")  # 收集所有日志信息文件
        self.__error_log_path = os.path.join(log_path, log_name + "_error_" + self.__now_time + ".log")  # 收集错误日志信息文件
        self.__logger = logging.getLogger()  # 创建日志记录器
        self.__logger.setLevel(logging.DEBUG)  # 设置默认日志记录器记录级别

    @staticmethod
    def __init_logger_handler(log_path):
        """
        创建日志记录器handler，用于收集日志
        :param log_path: 日志文件路径
        :return: 日志记录器
        """
        # 写入文件，如果文件超过10M大小时，切割日志文件，仅保留10个文件
        logger_handler = RotatingFileHandler(filename=log_path, maxBytes=50 * 1024 * 1024, backupCount=20,
                                             encoding='utf-8')
        return logger_handler

    def __set_log_handler(self, logger_handler, level=logging.DEBUG):
        """
        设置handler级别并添加到logger收集器
        :param logger_handler: 日志记录器
        :param level: 日志记录器级别
        """
        logger_handler.setLevel(level=level)
        self.__logger.addHandler(logger_handler)

    @staticmethod
    def __set_log_formatter(file_handler):
        """
        设置日志输出格式-日志文件
        :param file_handler: 日志记录器
        """
        formatter = logging.Formatter(default_formats["log_format"], datefmt='%a, %d %b %Y %H:%M:%S')
        file_handler.setFormatter(formatter)

    @staticmethod
    def __close_handler(file_handler):
        """
        关闭handler
        :param file_handler: 日志记录器
        """
        file_handler.close()

    def __console(self, level, message):
        """构造日志收集器"""
        all_logger_handler = self.__init_logger_handler(self.__all_log_path)  # 创建日志文件
        error_logger_handler = self.__init_logger_handler(self.__error_log_path)

        self.__set_log_formatter(all_logger_handler)  # 设置日志格式
        self.__set_log_formatter(error_logger_handler)

        self.__set_log_handler(all_logger_handler)  # 设置handler级别并添加到logger收集器
        self.__set_log_handler(error_logger_handler, level=logging.ERROR)

        if level == 'info':
            self.__logger.info(message)
        elif level == 'debug':
            self.__logger.debug(message)
        elif level == 'warning':
            self.__logger.warning(message)
        elif level == 'error':
            self.__logger.error(message)
        elif level == 'critical':
            self.__logger.critical(message)

        self.__logger.removeHandler(all_logger_handler)  # 避免日志输出重复问题
        self.__logger.removeHandler(error_logger_handler)

        self.__close_handler(all_logger_handler)  # 关闭handler
        self.__close_handler(error_logger_handler)

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)

    def critical(self, message):
        self.__console('critical', message)


def init_add_milvus_logger():
    global logger_add_milvus
    logger_add_milvus = HandleLog("add_milvus")


def init_api_logger():
    global logger_api, logger_corpus_reranker, logger_corpus_milvus
    logger_api = HandleLog("support_api")

    logger_corpus_reranker = HandleLog("corpus_rerank")
    logger_corpus_milvus = HandleLog("corpus_milvus")
