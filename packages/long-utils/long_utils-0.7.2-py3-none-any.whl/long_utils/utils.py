import hashlib
from typing import Union


def str_to_md5(content: Union[str, bytes]):
    """
    字符串转md5字符
    :param content: 字符串的内容
    :return: fe01ce2a7fbac8fafaed7c982a04e229
    """
    if not isinstance(content, bytes):
        content = content.encode('utf-8')
    md5_l = hashlib.md5()
    md5_l.update(content)
    return md5_l.hexdigest()
