import logging
import re
import time
from abc import ABC
from typing import Callable

from hanziconv import HanziConv

from duowen_huqie.nlp.re_pattern import NON_ALNUM_SPACE_PATTERN, NON_SPACE_FOLLOWED_BY_NON_ALNUM_PATTERN


class MatchTextExpr(ABC):
    def __init__(self, fields: list[str], matching_text: str, topn: int, extra_options=None, ):
        if extra_options is None:
            extra_options = dict()
        self.fields = fields
        self.matching_text = matching_text
        self.topn = topn
        self.extra_options = extra_options


def rmSpace(txt):
    txt = NON_ALNUM_SPACE_PATTERN.sub(r"\1\2", txt, flags=re.IGNORECASE)
    return NON_SPACE_FOLLOWED_BY_NON_ALNUM_PATTERN.sub(r"\1\2", txt, flags=re.IGNORECASE)


def tradi2simp(line):
    return HanziConv.toSimplified(line)


def strQ2B(ustring):
    """Convert full-width characters to half-width characters"""
    rstring = ""
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xFEE0
        if (
                inside_code < 0x0020 or inside_code > 0x7E):  # After the conversion, if it's not a half-width character, return the original character.
            rstring += uchar
        else:
            rstring += chr(inside_code)
    return rstring


def format_expression(expression):
    # 正则表达式匹配双引号内的内容
    quoted_content = re.compile(r'"[^"]*"')

    # 用于存储最终结果
    result = []

    # 遍历表达式的每个字符
    i = 0
    while i < len(expression):
        # 如果当前字符是双引号
        if expression[i] == '"':
            # 找到匹配的双引号内容
            match = quoted_content.match(expression, i)
            if match:
                # 将双引号内的内容直接添加到结果中
                result.append(match.group())
                i = match.end()  # 移动到双引号内容的末尾
            else:
                # 如果没有匹配的双引号，直接添加当前字符
                result.append(expression[i])
                i += 1
        else:
            # 如果当前字符是空格，替换为换行符
            if expression[i] == " ":
                result.append("\n")
            else:
                # 否则直接添加当前字符
                result.append(expression[i])
            i += 1

    # 将结果列表拼接为字符串
    return "".join(result)


def record_time():
    def decorator(fn: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Callable:
            start_time = time.time()
            ret = fn(*args, **kwargs)
            duration = time.time() - start_time
            # print(f"[duowen-huqie timer] <{fn.__name__}> run {duration}s")
            logging.debug(f"[duowen-huqie timer] <{fn.__name__}> run {duration}s")
            return ret
        return wrapper
    return decorator
