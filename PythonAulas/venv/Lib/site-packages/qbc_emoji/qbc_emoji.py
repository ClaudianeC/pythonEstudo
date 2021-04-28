# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import time
from curses import ascii
import os
import platform

from PIL import Image, ImageDraw, ImageFont, ImageColor

from ybc_exception import *


if(platform.system()=='Windows'):
    __CHINESE_FONT_PATH = os.path.split(__file__)[0]+'\\NotoSansCJK-Bold.ttc'
    __SYMBOL_FONT_PATH = os.path.split(__file__)[0]+"\\DejaVuSansMono.ttf"
else:
    __CHINESE_FONT_PATH = os.path.split(__file__)[0]+'/NotoSansCJK-Bold.ttc'
    __SYMBOL_FONT_PATH = os.path.split(__file__)[0]+"/DejaVuSansMono.ttf"


# 黑底图片转换成待替换像素点图片的宽度，为防止内存溢出，如非必要不改动此数值
__RESIZE_IMAGE_WIDTH = 50

# 生成图片的默认文字颜色
_DEFAULT_TEXT_COLOR = '#000000'

# 字号，生成图片的宽度随字号增大而增大，为防止内存溢出，如非必要不改动此数值
__FONT_SIZE = 20

# 输出在 canvas 区的行距
__LINE_HEIGHT = int(1.2 * __FONT_SIZE)


@exception_handler('qbc_emoji')
@params_check([
    ParamCheckEntry('word', str, is_not_empty),
    ParamCheckEntry('char', str, is_not_empty)
])
def word2emoji(word='', char=''):
    """
    功能：输入字和符号，在输出区打印出字符画。

    参数 word: 需要打印的字
    参数 char: 组成字的符号
    返回：无。
    """
    if len(char) != 1:
        return -1

    res_img = _text2image(word)
    txt = _image_to_string(res_img, char, width=30, create_image=False)
    txt = _del_empty_line(txt, 3)
    print(txt)



@exception_handler('qbc_emoji')
@params_check([
    ParamCheckEntry('word', str, is_not_empty),
    ParamCheckEntry('char', str, is_not_empty),
    ParamCheckEntry('filename', str, None)
])
def word2img(word, char, filename='', color="#000000"):
    """
    功能：输入字和符号，在画板上画出字符画，可右键保存为图片。

    参数 word: 需要打印的字，
    参数 char: 组成字的符号，
    可选参数 filename: 保存后的文件名称，
    返回：None
    """
    # 白底黑字图片
    transfer_img = _text2image(word)
    text = _image_to_string(transfer_img, char, width=__RESIZE_IMAGE_WIDTH, create_image=True)
    font = _choose_font(char, __FONT_SIZE)

    # 新图片的尺寸
    img_width = _get_image_size(text, font, char)[0]
    img_height = img_width * 1.0 / transfer_img.size[0] * transfer_img.size[1]

    bg_color = '#ffffff'

    img = Image.new('RGB', (round(img_width), round(img_height)), bg_color)
    draw = ImageDraw.Draw(img)
    # 判断 color 是否有效，若颜色输入错误，使用默认颜色 _DEFAULT_TEXT_COLOR
    try:
        ImageColor.getrgb(color)
    except ValueError:
        color = _DEFAULT_TEXT_COLOR

    # 如果 char 为汉字，生成图片略宽，为美观需要右移
    if _is_chinese(char):
        draw.text((150, 0), text, color, font)
    else:
        draw.text((0, 0), text, color, font)

    if filename == '':
        filename = str(int(time.time())) + '_emoji.jpg'

    img.save(filename)
    return filename


# 得到文字图画的尺寸
def _get_image_size(text, font, char):
    page_height = 0
    max_width = 0
    lines = text.split("\n")
    if _is_chinese(char):
        for i in range(0, len(lines)):
            page_height += font.getsize(lines[i])[1]
            page_width = font.getsize(lines[i])[1] * len(lines[i])
            if page_width > max_width:
                max_width = page_width
    else:
        for i in range(0, len(lines)):
            page_height += font.getsize(lines[i])[1]
            page_width = font.getsize(lines[i])[0]
            if page_width > max_width:
                max_width = page_width

    return max_width, page_height


def _is_emoji(content):
    """
    功能： 判断是否原生 emoji 表情，搜狗输入法表情 ❤️ ✨ 等会判断为false。

    :param content: 需要判断的表情符号。
    :return: True/False
    """
    if not content:
        return False
    # Smileys
    if u"\U0001F600" <= content and content <= u"\U0001F64F":
        return True
    # People and Fantasy
    elif u"\U0001F300" <= content and content <= u"\U0001F5FF":
        return True
    # Clothing and Accessories
    elif u"\U0001F680" <= content and content <= u"\U0001F6FF":
        return True
    # Pale Emojis
    elif u"\U0001F1E0" <= content and content <= u"\U0001F1FF":
        return True
    else:
        return False


# 判断一个是否为中文字符或者全角字符
def _is_chinese(char):
    if (char >= u'\u4e00' and char <= u'\u9fa5') or (char >= u'\u3000' and char <= u'\u303F') or (
            char >= u'\uFF00' and char <= u'\uFFEF'):
        return True
    else:
        return False


def _text2image(word):
    """
    @brief 将一个中文字符转为白底黑字图片
    @params word: 中文字
    @params fontpath: 字体文件的路径
    @return image
    """
    page_width = 500

    # 设置图宽高
    onechar_height = 0
    onechar_endheightlist = []

    for char in word:
        font = _choose_font(char, 500)
        onechar_addheight = round(font.getsize(char)[1] * 1.2)
        nextheight = onechar_height + onechar_addheight
        onechar_endheightlist.append(nextheight)
        onechar_height = nextheight

    page_height = onechar_endheightlist[-1]

    # 文字颜色，黑色
    word_color = '#000000'
    # 背景颜色，白色
    bg_color = '#ffffff'

    img = Image.new('RGB', (page_width, page_height), bg_color)
    draw = ImageDraw.Draw(img)

    # 竖向输出字符
    height = 0
    for char in word:
        font = _choose_font(char, 500)
        addheight = font.getsize(word)[1]
        # 如果 char 不是汉字，左偏，为美观需要右移
        if _is_chinese(char):
            draw.text((0, height), char, word_color, font)
        else:
            draw.text((100, height), char, word_color, font)
        nextheight = height + addheight
        height = nextheight
    return img


def _choose_font(char, font_size):
    """
    根据 char 类型选择字体，中文字符或全角字符，用 __CHINESE_FONT 字体绘图,其他字符用 __SYMBOL_FONT
    :param char: 输入字符
    :param font_size: 字体尺寸
    :return: 需使用的字体
    """
    if _is_chinese(char):
        fontpath = __CHINESE_FONT_PATH
    else:
        fontpath = __SYMBOL_FONT_PATH

    return ImageFont.truetype(fontpath, font_size)


def _del_empty_line(text, num):
    """
    删除输出区的多余空行
    :param text: 输出区文本
    :param num: 需要保留的空行数
    :return: 删除无用空行后的文本
    """
    lines = text.split("\n")
    # 删除文本开始前的空行
    for i in range(0, len(lines)):
        if not lines and not lines[num].strip():
            lines.pop(0)
        else:
            break
    # 删除文本最后的空行
    for i in range(len(lines) - 1, 0, -1):
        if not lines and not lines[i - num].strip():
            lines.pop(i)
        else:
            break
    return "\n".join(lines)


def _image_to_string(img, char, width=30, create_image=False):
    """
    @brief 将图片转化为字符串
    @params img: 待打印的白底黑字的图片
    @params char: 替换图片的字符
    @params width: 由于像素点转为打印字符占用屏幕宽度挺大的, 所以需要对图片进行相应缩小，默认宽度为 30，大小为 30*38 像素.
    @return string
    """
    # 中文字符或全角字符，windows 系统对应 1 全角空格
    if _is_chinese(char):
        ascii_char = [char, '　']

    # mac 系统下的 emoji 宽度对应 1 个英文空格，为防止重叠额外增加一个英文空格；Windows 的彩色 emoji 暂无法对齐整数倍空格
    elif _is_emoji(char):
        char += ' '
        ascii_char = [char, '  ']

    # ascii 字符，对应 1 个半角空格，为保证输出内容的美观，对字符复制 2 倍
    elif _isascii(char):
        char += char
        ascii_char = [char, '  ']

    # 其他字符，如 ❤, windows 系统对应 1 半角空格
    else:
        # 若打印到输出区，防止字符表情重叠需要加一个半角空格；若生成图片，为保证输出内容的美观，对字符复制 2 倍
        if not create_image:
            char += ' '
        else:
            char += char
        ascii_char = [char, '  ']

    return _do_image2string(img, width, ascii_char)


def _do_image2string(img, width, ascii_char):
    def select_ascii_char(r, g, b):
        """ 在灰度图像中，灰度值最高为 255，代表白色，最低为 0，代表黑色 """
        gray = int((19595 * r + 38469 * g + 7472 * b) >> 16)  # 'RGB－灰度值'转换公式
        if gray == 255:
            return ascii_char[1]
        else:
            return ascii_char[0]

    txt = ""
    old_width, old_height = img.size
    # 根据原图比例进行缩放，长宽比约为 5 : 4
    height = int(width * 1.0 / old_width * old_height)
    img = img.resize((width, height), Image.NEAREST)
    # img.show()
    for h in range(height):
        for w in range(width):
            # 每个像素点替换为字符
            txt += select_ascii_char(*img.getpixel((w, h))[:3])
        txt += '\n'
    return txt


def _isascii(s):
    return all(ascii.isascii(c) for c in s)


if __name__ == '__main__':
    # word2emoji('辅', '小')
    # word2emoji('辅', 'a')
    # word2emoji('辅', '.')
    # word2emoji('辅', '✨')
    # word2emoji('辅', '😊')

    # word2image('辅', '小')
    # word2image('辅', 'a')
    word2img('猿', '❤', '1.jpg', 'red')
    # word2image('辅', '❤')
    # word2image('超级大', '😊')
