import inspect
import time
from .enum import TextDisplayMethod
from .enum import TextForeground
from .enum import TextBackground


class BaseLog(object):

    def __init__(self, show_line=True, show_file_name=True, show_time=True):
        """
        :param show_line: 是否显示行数
        :param show_file_name: 是否显示文件名
        :param show_time: 是否显示时间
        """
        self.show_line = show_line
        self.show_file_name = show_file_name
        self.show_time = show_time

    def _format_text(
            self,
            text: str,
            method="default",
            text_fg=None,
            text_bg=None
    ):
        """
        \033[显示方式;前景色;背景色***\033[0m
        :param text: 输出的文本内容
        :param method: 显示方式
        :param text_fg: 前景
        :param text_bg: 背景
        :return:
        """
        if not hasattr(TextDisplayMethod, method):
            raise Exception(f"没有找到该显示方式: {method}, 目前仅支持：default or highlight or underline or flicker "
                            f"or reverse_display or invisible")
        if text_bg and not hasattr(TextBackground, text_bg):
            raise Exception(f"没有找到背景色： {text_bg}, 目前仅支持：black表示黑色。red表示红色。"
                            f"green表示绿色。yellow表示黄色。blue表示蓝色。purplish_red表示紫红色。turquoise_blue表示青蓝色。white表示白色")
        if text_fg and not hasattr(TextForeground, text_fg):
            raise Exception(f"没有找到前景色： {text_fg}, 目前仅支持：black表示黑色。red表示红色。"
                            f"green表示绿色。yellow表示黄色。blue表示蓝色。purplish_red表示紫红色。turquoise_blue表示青蓝色。white表示白色")
        if text_bg:
            text_bg = getattr(TextBackground, text_bg)
        if text_fg:
            text_fg = getattr(TextForeground, text_fg)
        display_method = getattr(TextDisplayMethod, method)
        frame = inspect.currentframe().f_back.f_back  # 获取调用 dd 方法的栈帧
        info = f"\033[{display_method}"
        if text_fg:
            info += f";{text_fg}"
        if text_bg:
            info += f";{text_bg}"
        content = ""
        if self.show_line:
            file_name = frame.f_globals['__file__']
            content += f"{file_name} "
        if self.show_time:
            content += f"时间: {time.strftime('%Y-%m-%d %H:%M:%S',  time.localtime(time.time()))} "
        if self.show_file_name:
            line_number = frame.f_lineno  # 获取行号
            content += f"行数:{line_number} "
        content += f"输出内容：{text}"
        info += f"m{content}\033[0m"
        print(info)
