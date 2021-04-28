"""
自定义异常类
"""
import re
import sys

if sys.platform == 'skulpt':

    def exception_handler(module_name=''):
        def handler(fn):

            def wrapped(*args, **kwargs):
                try:
                    return fn(*args, **kwargs)
                except ReturnValueError as ex:
                    return ex.return_value()
                except (ParameterTypeError, ParameterValueError,
                        IllegalFilenameError, FilenameTooLongError) as ex:
                    raise ex
                except Exception as ex:
                    # skulpt 暂时无法处理 InternalError
                    raise ex

            return wrapped

        return handler

    def params_check(param_check_entries):
        """
        skulpt的参数检查

        :param param_check_entries:
        :return:
        """
        def check(fn):
            def wrapped(*args, **kwargs):
                return fn(*args, **kwargs)
            return wrapped
        return check

else:
    import inspect
    from functools import wraps

    def exception_handler(module_name=''):
        def handler(fn):
            # 使用装饰器修饰方法时反射拿不到原方法的 方法名(__name__) 和 docstring(__doc__)，
            # 导致 Sphinx 不能正常扫描，使用 wraps 装饰器可解决
            @wraps(fn)
            def wrapped(*args, **kwargs):
                try:
                    return fn(*args, **kwargs)
                except ReturnValueError as ex:
                    return ex.return_value()
                except (ParameterTypeError, ParameterValueError,
                        IllegalFilenameError, FilenameTooLongError) as ex:
                    raise ex
                except Exception as ex:
                    if ex.__class__.__name__ in _EXCEPTION_DICT_ZH.keys():
                        raise ex
                    else:
                        raise InternalError(ex, module_name)

            return wrapped

        return handler

    def params_check(param_check_entries=[]):
        """
        检查方法参数类型和值是否合法的修饰器

        :param param_check_entries: 参数检查条目列表
        :return:
        """

        def check(fn):
            sig = inspect.signature(fn)

            @wraps(fn)
            def type_check(*params):
                """
                参数类型检查
                :param params:
                :return:
                """
                error_fields = []
                param_index = 0
                for param in params:
                    if param is None or param_index >= len(param_check_entries):
                        break
                    param_check_entry = param_check_entries[param_index]
                    if not isinstance(param_check_entry, ParamCheckEntry):
                        continue
                    if not isinstance(param, param_check_entry.param_type):
                        error_fields.append("'" + param_check_entry.param_name + "'")
                    param_index = param_index + 1

                if len(error_fields) > 0:
                    raise ParameterTypeError(fn.__name__, '、'.join(error_fields))

            @wraps(fn)
            def value_check(*params):
                """
                参数值检查
                :param params:
                :return:
                """

                def update_error_fields_if_is_invalid_value(param_value, entry):
                    is_valid_value = True

                    if entry.is_valid_value_func:
                        if entry.is_valid_value_func_params:
                            is_valid_value = entry.is_valid_value_func(param_value, entry.is_valid_value_func_params)
                        else:
                            is_valid_value = entry.is_valid_value_func(param_value)

                    if not is_valid_value:
                        error_fields.append("'" + entry.param_name + "'")

                error_fields = []
                param_index = 0
                for param in params:
                    if param_index >= len(param_check_entries):
                        break
                    param_check_entry = param_check_entries[param_index]
                    if not isinstance(param_check_entry, ParamCheckEntry):
                        continue
                    update_error_fields_if_is_invalid_value(param, param_check_entry)
                    param_index = param_index + 1

                if len(error_fields) > 0:
                    raise ParameterValueError(fn.__name__, '、'.join(error_fields))

            @wraps(fn)
            def wrapped(*args, **kwargs):
                bound_args = sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                params = tuple(bound_args.arguments.values())

                type_check(*params)
                value_check(*params)
                return fn(*params)

            return wrapped

        return check


def _info_formatter(line_no, ex_type=None, ex_msg=None, code_info=None, zh_type=None, zh_msg=None):
    """
    对于寻常错误的专用格式化方法
    :param line_no: 行号 str
    :param ex_type: 错误类型 en_str
    :param ex_msg: 错误信息 en_msg
    :param code_info: 错误代码标识，可传入 None 或者 str
    :param zh_type: 错误类型 zh_str
    :param zh_msg: 错误信息 zh_msg
    :return: 格式化后信息字符串

    PS:
        信息串 line_no 是否打印，会依据 line_no 是否为 (0) 来判断
        信息串 code_info 是否打印，会依据 code_info 来进行判断
        信息串 ex_type : ex_msg 是否打印，会依据 ex_type 来进行判断
        信息串 zh_type : zh_msg 是否打印，会依据 zh_type 来进行判断
    """
    err_msg = str()
    if int(line_no) != 0:
        err_msg += "【Error】行号 Line " + str(line_no) + ":\n"
    if code_info:
        err_msg += str(code_info) + "\n"
    if ex_type:
        err_msg += str(ex_type) + " : " + str(ex_msg) + ".\n"
    if zh_type:
        err_msg += str(zh_type) + " : " + str(zh_msg) + "。\n"
    return err_msg


# 参数类型异常类
class ParameterTypeError(Exception):
    _error_code = -1
    _error_type = "参数类型错误"
    _error_lineno = int()

    def __init__(self, function_name="", error_msg=""):
        if sys.platform != 'skulpt':
            # 初始化父类, skulpt 不支持 super()
            super().__init__(self)  # 初始化父类
        self.function_name = function_name
        self.error_msg = error_msg

    def __str__(self):
        return _info_formatter(line_no=str(self._error_lineno), zh_type=self._error_type,
                               zh_msg="调用" + self.function_name + "方法时，" + self.error_msg + "参数类型错误")

    def setlineno(self, lineno=0):
        self._error_lineno = lineno


# 参数值异常类
class ParameterValueError(Exception):
    _error_code = -2
    _error_type = "参数数值错误"
    _error_lineno = int()

    def __init__(self, function_name="", error_msg=""):
        if sys.platform != 'skulpt':
            # 初始化父类, skulpt 不支持 super()
            super().__init__(self)
        self.function_name = function_name
        self.error_msg = error_msg

    def __str__(self):
        return _info_formatter(line_no=str(self._error_lineno), zh_type=self._error_type,
                               zh_msg="调用" + self.function_name + "方法时，" + self.error_msg + "参数不在允许范围内")

    def setlineno(self, lineno=0):
        self._error_lineno = lineno


# 内部异常包装类
class InternalError(Exception):
    _error_code = -3
    _error_type = "内部错误"
    _error_lineno = int()

    def __init__(self, exception, module_name):
        if sys.platform != 'skulpt':
            # 初始化父类, skulpt 不支持 super()
            super().__init__(self)
        print(exception)
        if isinstance(exception, InternalError):
            self._meta_exception = exception._meta_exception
        else:
            self._meta_exception = exception
        self.module_name = module_name

    def __str__(self):
        internal_msg = ""
        print(dir(self))
        if self.module_name not in ('browser', 'gui', 'media', 'mpl', 'protocol', 'turtle_wrapper', 'wxpy'):
            internal_msg = "导入的" + self.module_name
        return _info_formatter(line_no=str(self._error_lineno), zh_type="模块报错", zh_msg=internal_msg + "模块出现内部错误，请稍后再试")

    def setlineno(self, lineno=0):
        self._error_lineno = lineno


# 文件命名异常类
class IllegalFilenameError(Exception):
    _error_code = -4
    _error_type = "参数数值错误"
    _error_lineno = int()

    def __init__(self, filename="", error_msg=""):
        if sys.platform != 'skulpt':
            # 初始化父类, skulpt 不支持 super()
            super().__init__(self)
        self.filename = filename
        self.error_msg = error_msg

    def __str__(self):
        return _info_formatter(line_no=str(self._error_lineno), zh_type=self._error_type,
                               zh_msg=self.filename + '文件命名中包含非法字符，只能包含"字母，数字，中文，_-.()"')

    def setlineno(self, lineno=0):
        self._error_lineno = lineno


# 文件名过长异常类
class FilenameTooLongError(Exception):
    _error_code = -5
    _error_type = "参数数值错误"
    _error_lineno = int()

    def __init__(self, filename="", error_msg=""):
        if sys.platform != 'skulpt':
            # 初始化父类, skulpt 不支持 super()
            super().__init__(self)
        self.filename = filename
        self.error_msg = error_msg

    def __str__(self):
        return _info_formatter(line_no=str(self._error_lineno), zh_type=self._error_type,
                               zh_msg=self.filename + '文件命名最多40个字符或20个中文字符')

    def setlineno(self, lineno=0):
        self._error_lineno = lineno


class RegularErrHandler(object):
    """
    常规异常处理类: 用于处理 WebIDE 语法级别的错误异常

    __exception_zh:
        * 包含了所有能够提供的错误提示信息
            * 包括对应的类型错误的：
                * zh 错误类型
                * zh 错误提示
        * 如果要禁用某个中文提示，将对应错误类型的 "Name" 键置空（或者None）即可

    __ex_detail_list:
        * 包含详细提示信息的异常列表
    """
    EXCEPTION_DICT_ZH = {
        "Exception": {
            "Name": "异常",
            "Desc": "出现了 Python 异常"
        },
        "StopIteration": {
            "Name": "迭代异常停止",
            "Desc": "迭代器无法继续迭代"
        },
        "StopAsyncIteration": {
            "Name": None,
            "Desc": "异步迭代器对象的 __anext()__ 方法使迭代异常停止"
        },
        "ArithmeticError": {
            "Name": "算数计算错误",
            "Desc": "发生计算机算数计算错误"
        },
        "FloatingPointError": {
            "Name": "浮点错误",
            "Desc": "浮点数计算失败"
        },
        "OverflowError": {
            "Name": "溢出错误",
            "Desc": "计算结果超出了计算机处理上限"
        },
        "ZeroDivisionError": {
            "Name": "除数为零错误",
            "Desc": "0不能作为除数"
        },
        "AssertionError": {
            "Name": "断言错误",
            "Desc": "断言语句失败"
        },
        "AttributeError": {
            "Name": "属性错误",
            "Desc": "访问的对象、模块中没有相关的属性或方法"
        },
        "BufferError": {
            "Name": None,
            "Desc": "缓冲操作出现异常"
        },
        "EOFError": {
            "Name": "空输入错误",
            "Desc": "目前网页版IDE暂不支持input输入"
        },
        "ImportError": {
            "Name": "导入错误",
            "Desc": "模块/对象导入失败：没找到相关模块或对象"
        },
        "ModuleNotFoundError": {
            "Name": "模块不存在错误",
            "Desc": "模块导入的模块不存在,请检查模块名称是否错误或模块是否安装"
        },
        "LookupError": {
            "Name": "查找错误",
            "Desc": "映射或序列上使用的键或索引无效"
        },
        "IndexError": {
            "Name": "索引错误",
            "Desc": "引用或访问了列表中不存在的元素"
        },
        "KeyError": {
            "Name": "键错误",
            "Desc": "访问的键值在字典中不存在"
        },
        "MemoryError": {
            "Name": "内存溢出错误",
            "Desc": "内存溢出了"
        },
        "NameError": {
            "Name": "名字错误",
            "Desc": "模块、方法、变量被导入、定义、赋值后，才能使用"
        },
        "UnboundLocalError": {
            "Name": "变量边界定义错误",
            "Desc": "请告知解释器，使用的是局部变量还是全局变量，在函数内给变量赋值，会将全局变量变为局部变量"
        },
        "OSError": {
            "Name": None,
            "Desc": "操作系统类错误"
        },
        "BlockingIOError": {
            "Name": None,
            "Desc": "非阻塞操作的对象被阻塞"
        },
        "ChildProcessError": {
            "Name": None,
            "Desc": "子进程操作失败"
        },
        "ConnectionError": {
            "Name": "网络错误",
            "Desc": "访问不到第三方服务，请稍后再试"
        },
        "BrokenPipeError": {
            "Name": "网络错误",
            "Desc": "访问不到第三方服务，请稍后再试"
        },
        "ConnectionAbortedError": {
            "Name": "网络错误",
            "Desc": "访问不到第三方服务，请稍后再试"
        },
        "ConnectionRefusedError": {
            "Name": "网络错误",
            "Desc": "访问不到第三方服务，请稍后再试"
        },
        "ConnectionResetError": {
            "Name": "网络错误",
            "Desc": "访问不到第三方服务，请稍后再试"
        },
        "SSLError": {
            "Name": "HTTPS证书错误",
            "Desc": "如果使用了代理，请关闭代理"
        },
        "FileExistsError": {
            "Name": "文件已存在错误",
            "Desc": "创建的文件或目录已存在"
        },
        "FileNotFoundError": {
            "Name": "文件未找到",
            "Desc": "文件或目录并不存在"
        },
        "InterruptedError": {
            "Name": "中断错误",
            "Desc": "系统调用被输入信号中断时发生错误"
        },
        "IsADirectoryError": {
            "Name": "是目录错误",
            "Desc": "访问的文件名实际为目录名"
        },
        "NotADirectoryError": {
            "Name": "不是目录错误",
            "Desc": "访问的目录实际为文件名"
        },
        "PermissionError": {
            "Name": "权限错误",
            "Desc": "没有访问文件或目录的权限"
        },
        "ProcessLookupError": {
            "Name": None,
            "Desc": "给定的进程并不存在"
        },
        "TimeoutError": {
            "Name": None,
            "Desc": "系统级函数超时"
        },
        "ReferenceError": {
            "Name": None,
            "Desc": "弱引用代理在垃圾回收后用于访问引用对象的属性"
        },
        "RuntimeError": {
            "Name": None,
            "Desc": "运行时错误"
        },
        "NotImplementedError": {
            "Name": None,
            "Desc": "尚未实现的方法"
        },
        "RecursionError": {
            "Name": "递归错误",
            "Desc": "递归层数太深，已超出python限制"
        },
        "SyntaxError": {
            "Detail": {
                "invalid syntax": "请检查指示位置是否存在以下错误：\n  (1)是否存在遗漏或冗余的符号、空格；\n  (2)变量、方法、模块的名称是否存在拼写错误或存在用python关键字起的名称；\n  (3)判断、循环语句语法是否漏写、多写了条件。",
                "invalid character in identifier": "使用了不可用的标点符号，注意要使用英文字符",
                "unexpected EOF while parsing": "代码意外结束了，请检查是否存在代码遗漏。",
                "EOL while scanning string literal": "请检查是否遗漏了引号，或者字符串最后存在反斜杠。",
                "'break' outside loop": "只有在循环语句中才能使用“break”"
            },
            "Name": "语法错误",
            "Desc": "请检查指示位置是否存在语法错误"
        },
        "IndentationError": {
            "Name": "缩进语法错误",
            "Desc": "使用了错误的缩进，检查是否使用了不应出现的缩进"
        },
        "TabError": {
            "Name": "缩进语法错误",
            "Desc": "缩进时混合使用了tab和空格"
        },
        "SystemError": {
            "Name": None,
            "Desc": "解释器系统错误"
        },
        "TypeError": {
            "Name": "参数类型错误",
            "Desc": "向方法中传递的参数类型错误"
        },
        "ValueError": {
            "Name": "参数数值错误",
            "Desc": "向方法中传递的参数范围错误"
        },
        "UnicodeError": {
            "Name": None,
            "Desc": "Unicode 错误"
        },
        "UnicodeDecodeError": {
            "Name": None,
            "Desc": "Unicode 解码错误"
        },
        "UnicodeEncodeError": {
            "Name": None,
            "Desc": "Unicode 编码错误"
        },
        "UnicodeTranslateError": {
            "Name": None,
            "Desc": "Unicode 转码错误"
        },
        "Warning": {
            "Name": None,
            "Desc": "发现警告"
        },
        "DeprecationWarning": {
            "Name": None,
            "Desc": "警告：已弃用的功能"
        },
        "PendingDeprecationWarning": {
            "Name": None,
            "Desc": "警告：将来会被弃用的功能"
        },
        "RuntimeWarning": {
            "Name": None,
            "Desc": "警告：可疑的运行时行为"
        },
        "SyntaxWarning": {
            "Name": None,
            "Desc": "警告：可疑的语法"
        },
        "UserWarning": {
            "Name": None,
            "Desc": "警告：用户代码生成的警告"
        },
        "FutureWarning": {
            "Name": None,
            "Desc": "警告：将来会在语义上更改的构造"
        },
        "ImportWarning": {
            "Name": None,
            "Desc": "警告：模块导入可能有问题"
        },
        "UnicodeWarning": {
            "Name": None,
            "Desc": "警告：Unicode 相关警告"
        },
        "BytesWarning": {
            "Name": None,
            "Desc": "警告：与 bytes 和 bytearray 相关的警告"
        },
        "ResourceWarning": {
            "Name": None,
            "Desc": "警告：资源使用相关的警告"
        },
        "UnsupportedOperation": {
            "Name": "IO操作错误",
            "Desc": "以读模式打开文件时，只能进行读操作，不能写操作；以写模式打开文件时，只能进行写操作，不能进行读操作"
        },
        "HTTPError": {
            "Name": "HTTP错误",
            "Desc": "网址拼写错误或者该网址无法访问"
        }
    }
    __ex_detail_list = [
        "SyntaxError",
    ]

    def __init__(self, ex, tb, ts):
        """
        用与外部调用的异常处理接口
        :param ex: 捕获到的异常
        :param tb: 列表 traceback.extract_tb(tb, 2)
        :param ts: 字符串traceback.format_exc()
        """
        self.line_no = str()
        self.ex_type = str(ex.__class__.__name__)
        self.ex_msg = str(ex)
        self.code_info = None
        self.zh_type = None
        self.zh_msg = None

        if isinstance(ex, SyntaxError):
            self.line_no = str(ex).split('line ')[-1].split(')')[0]
            self.ex_msg = "".join(re.compile("<[^>]*>,\s").split(self.ex_msg))
            ts = ts.split('\n')
            if ts[-3].find("^") != -1:
                self.code_info = str(ts[-4]) + "\n" + str(ts[-3])
        else:
            self.line_no = str(tb[1].lineno)

        if self.ex_type in RegularErrHandler.EXCEPTION_DICT_ZH:
            self.zh_type = RegularErrHandler.EXCEPTION_DICT_ZH[self.ex_type]["Name"]
            self.zh_msg = RegularErrHandler.EXCEPTION_DICT_ZH[self.ex_type]["Desc"]

            if self.ex_type in RegularErrHandler.__ex_detail_list:
                for key, value in RegularErrHandler.EXCEPTION_DICT_ZH[self.ex_type]["Detail"].items():
                    if re.match(key, self.ex_msg):
                        self.zh_msg = value
                        break

    def __str__(self):
        """
        :return: 格式化之后的字符串
        """
        return _info_formatter(self.line_no, self.ex_type, self.ex_msg, self.code_info, self.zh_type, self.zh_msg)


class ReturnValueError(Exception):
    """
    异常情况下返回值包装类
    """
    _return_value = ''

    def __init__(self, return_value):
        self._return_value = return_value

    def return_value(self):
        return self._return_value


_EXCEPTION_DICT_ZH = RegularErrHandler.EXCEPTION_DICT_ZH


class Range(object):
    def __init__(self, lower, upper):
        self.lower = lower
        self.upper = upper


def is_not_blank(value):
    """
    检查值是否为空，None {} [] () '' 都是空
    :param value:
    :return:
    """
    return is_not_empty(value) \
           and (isinstance(value, str) and value.strip) \
           or (isinstance(value, list) and all(is_not_blank(x) for x in value))


def is_not_empty(value):
    """
    检查值是否为空，None {} [] () '' 都是空
    :param value:
    :return:
    """
    return not not value


def is_in_range(value, value_range=Range(0, 0)):
    """
    检查值是否在某个范围内
    :param value:
    :param value_range: 参数值范围，闭区间
    :return:
    """
    return value_range.lower <= value <= value_range.upper


def is_greater_than(value, lower):
    """
    检查值是否大于某个值
    :param value:
    :param lower:
    :return:
    """
    return value > lower


def is_length_in_range(value, len_range=Range(0, 0)):
    """
    检查字符串的长度是否在某个范围内
    :param value: 字符串
    :param len_range: 字符串的长度范围
    :return:
    """
    return value and len_range.lower <= len(value) <= len_range.upper


def is_correct_file_format(filename, format_list=[]):
    """
    检查文件类型是否在所允许的类型列表内
    :param filename: 完整文件名
    :param format_list: 文件类型列表
    :return:
    """
    return not filename or filename.rsplit('.', 1)[-1] in format_list


def is_foldername_allowed(foldername):
    """
    检查文件夹名是否合法（只包含字母、数字、中文和'-', '_', '(', ')'）
    :param foldername: 文件夹名
    :return:
    """
    import re
    if re.match('^[\u4e00-\u9fa5\w\.\-\(\)]+$', foldername):
        return True
    return False


def is_in_list(value, value_list):
    """
    检查某个值是否在列表内
    :param value:
    :param value_list: 值列表
    :return:
    """
    return value_list and value in value_list


class ParamCheckEntry(object):
    """
    参数检查条目
    """
    def __init__(self, param_name=None, param_type=None, is_valid_value_func=is_not_empty, is_valid_value_func_params=None):
        """
        :param param_name: 参数名字
        :param param_type: 允许的参数类型
        :param is_valid_value_func: 参数值检查方法
        :param is_valid_value_func_params: 参数检查方法的参数
        """
        self.param_name = param_name
        self.param_type = param_type
        self.is_valid_value_func = is_valid_value_func
        self.is_valid_value_func_params = is_valid_value_func_params
