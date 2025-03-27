from long_utils.zlog import BaseLog


class Log(BaseLog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def success(self, message, method: str = "highlight"):
        """
        成功的类型输出内容
        :param message: 内容
        :param method: highlight高亮，underline下划线
        :return:
        """
        self._format_text(
            text=message,
            method=method,
            text_fg='green'
        )

    def success_bg(self, message):
        self._format_text(
            text=message,
            method="reverse_display",
            text_fg='green'
        )

    def error(self, message, method: str = "highlight"):
        self._format_text(
            text=message,
            method=method,
            text_fg='red'
        )

    def error_bg(self, message):
        self._format_text(
            text=message,
            method="reverse_display",
            text_fg='red'
        )

    def warning(self, message, method: str = "highlight"):
        self._format_text(
            text=message,
            method=method,
            text_fg='yellow'
        )

    def warning_bg(self, message):
        self._format_text(
            text=message,
            method="reverse_display",
            text_fg='yellow'
        )

    def info(self, message, method: str = "highlight"):
        self._format_text(
            text=message,
            method=method,
            text_fg='turquoise_blue'
        )

    def info_bg(self, message):
        self._format_text(
            text=message,
            method="reverse_display",
            text_fg='turquoise_blue'
        )

    def debug(self, message, method: str = "highlight"):
        self._format_text(
            text=message,
            method=method,
            text_fg='purplish_red'
        )

    def debug_bg(self, message):
        self._format_text(
            text=message,
            method="reverse_display",
            text_fg='purplish_red'
        )

    def color(self, message, method='default', fg='black', bg='blue'):
        """
        自定义
        :param message: 内容
        :param method: 显示方式
        :param fg: 前景色
        :param bg: 背景色
        :return:
        """
        self._format_text(
            text=message,
            method=method,
            text_fg=fg,
            text_bg=bg,
        )


if __name__ == '__main__':
    log = Log()
    log.success('xxxx')
    log.error('xxxx')
    log.warning('xxxx')
    log.debug('xxxx')
    log.info('xxxx')

    log.success_bg('xxxx')
    log.error_bg('xxxx')
    log.warning_bg('xxxx')
    log.debug_bg('xxxx')
    log.info_bg('xxxx')
    log.color('xxxx', fg='asdf')
