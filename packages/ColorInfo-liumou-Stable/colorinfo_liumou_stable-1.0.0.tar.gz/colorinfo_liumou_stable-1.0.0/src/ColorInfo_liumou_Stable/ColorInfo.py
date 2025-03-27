# -*- encoding: utf-8 -*-
"""
@File    :   ColorInfo.py
@Time    :   2022-10-19 16:01
@Author  :   坐公交也用券
@Version :   1.1.9
@Contact :   faith01238@hotmail.com
@Homepage : https://liumou.site
@Desc    :   彩色日志
"""
import inspect
import os
import platform
from datetime import datetime
from os import path
from sys import exit


class ColorLogger:
	def __init__(self, file=None, txt=False, cover=False, fileinfo=False, basename=True):
		"""
		初始化日志模块。

		:param file: str, optional
			设置日志文件的路径。如果为None，则不记录到文件。
		:param txt: bool, optional
			是否启用文本记录功能。默认为False。
		:param cover: bool, optional
			当使用文本记录时，是否覆盖原内容。默认为False（追加模式）。
		:param fileinfo: bool, optional
			是否显示日志文件信息。默认为False。
		:param basename: bool, optional
			设置日志文件显示信息的方式。True表示只显示文件名，False表示显示绝对路径。默认为True。

		:return: None
		"""
		# 定义颜色代码，用于控制台输出的颜色格式化
		self.Red = "\033[31m"  # 红色
		self.Greet = "\033[32m"  # 绿色
		self.Yellow = '\033[33m'  # 黄色
		self.Blue = '\033[34m'  # 蓝色
		self.RESET_ALL = '\033[0m'  # 清空颜色

		# 初始化日志文件相关参数
		self.basename = basename
		self.fileinfo = fileinfo
		self.cover = cover
		self.txt_mode = txt  # 是否启用文本记录功能
		self.file_name = None  # 日志文件显示名称
		self.file_path = file  # 日志文件绝对路径

		# 初始化日期和行数信息
		self.date = str(datetime.now()).split('.')[0]  # 当前日期时间
		self.line_ = 1  # 行数计数器

		# 初始化模块、文件和日志内容相关参数
		self.module_name = None  # 模块名称
		self.filename = None  # 文件名称
		self.msg1 = None  # 日志内容

		# 初始化日志格式化选项
		self.format_filename = True  # 是否启用文件名显示
		self.format_date = True  # 是否启用日期显示
		self.format_time = True  # 是否启用时间显示
		self.format_class = True  # 是否显示类名称
		self.format_fun = True  # 是否显示函数名称
		self.format_line = True  # 是否显示行数
		self.format_level = True  # 是否显示日志等级

		# 定义日志等级及其对应关系
		self.level_dic = {"DEBUG": 0, "INFO": 1, "WARNING": 2, "ERROR": 3}  # 日志等级映射
		self.level_list = ["DEBUG", "INFO", "WARNING", "ERROR"]  # 日志等级列表

		# 设置日志记录的最低等级
		self.level_text = 0  # 文件记录最低等级
		self.level_console = 0  # 控制台显示最低等级

		# 获取调用方法所在的类名和方法名
		self.caller_frame = inspect.stack()[1]  # 获取调用栈信息
		self.caller_class = self.caller_frame[0].f_locals.get('self', None).__class__.__name__  # 调用类名
		self.caller_method = self.caller_frame[3]  # 调用方法名
		self.fun_name = self.caller_frame[3]  # 函数名称

		# 调用初始化函数完成实例参数的设置
		self._init_fun()

	def _init_fun(self):
		"""
		初始化函数，用于设置日志文件路径和文件操作对象。
		
		参数:
			无（作为类方法，依赖类的属性进行初始化）
			
		返回值:
			无
		
		功能描述:
			1. 如果文件路径为空且文本模式开启，则设置默认日志文件路径为用户主目录下的 'ColorInfo.log'。
			2. 如果无法获取用户主目录，则抛出 EnvironmentError 异常。
			3. 如果开启了文本记录模式，则根据覆盖模式选择文件打开方式，并实例化文件操作对象。
			4. 如果文件打开失败，则打印错误信息并退出程序。
			5. 如果需要记录文件名，则提取并设置文件的基本名称。
		"""
		# 如果文件路径为空且文本模式开启，则设置默认日志文件路径
		if self.file_path is None and self.txt_mode:
			home_dir = os.getenv('HOME') or os.getenv('USERPROFILE')
			if not home_dir:
				raise EnvironmentError("无法获取用户主目录，请检查环境变量 'HOME' 或 'USERPROFILE'")
			self.file_path = path.abspath(path.join(home_dir, 'ColorInfo.log'))
		else:
			self.file_name = " "

		# 如果开启了文本记录模式，则实例化文件操作对象
		if self.txt_mode:
			try:
				# 根据是否覆盖文件选择打开模式
				mode = 'w+' if self.cover else 'a+'
				self.txt_wr = open(file=self.file_path, mode=mode, encoding='utf-8')
			except (IOError, OSError) as e:
				print(f"无法打开文件 '{self.file_path}'，错误信息: {e}")
				exit(1)

			# 设置文件名
			if self.basename:
				self.file_name = path.basename(self.file_path)

	def set_format(self, date_on=True, time_on=True, filename_on=True, class_on=True, fun_on=True, line=True, level=True):
		"""
		设置格式开关，默认全开。
		
		:param date_on: 是否显示日期，默认 True (格式示例: 2022-11-03)
		:param time_on: 是否显示时间，默认 True (格式示例: 20:42:24)
		:param filename_on: 是否显示文件名，默认 True (格式示例: ColorInfo.py)
		:param class_on: 是否显示类名，默认 True
		:param fun_on: 是否显示函数名，默认 True
		:param line: 是否显示行号，默认 True (格式示例: line: 230)
		:param level: 是否显示日志等级，默认 True (格式示例: DEBUG)
		"""
		# 参数类型检查
		for param_name, param_value in locals().items():
			if param_name != "self" and not isinstance(param_value, bool):
				raise ValueError(f"参数 {param_name} 必须是布尔值，但接收到 {type(param_value)} 类型")
	
		# 批量赋值
		self.format_date = date_on
		self.format_time = time_on
		self.format_filename = filename_on
		self.format_class = class_on
		self.format_fun = fun_on
		self.format_line = line
		self.format_level = level
	def validate_level(self, level: str, default="DEBUG"):
		"""
		验证并返回有效的日志等级。

		:param level: 待验证的日志等级，必须为字符串类型。
		:param default: 默认日志等级，当输入的日志等级无效时返回此值，默认为 "DEBUG"。
		:return: 验证后的日志等级，若输入有效则返回其大写形式，否则返回默认值。

		代码逻辑：
		1. 检查输入的 `level` 是否为字符串类型，且其大写形式是否在 `self.level_list` 中。
		2. 如果不符合条件，返回默认日志等级 `default`。
		3. 如果符合条件，返回输入日志等级的大写形式。
		"""
		if not isinstance(level, str) or level.upper() not in self.level_list:
			# 如果 level 不是字符串或不在允许的日志等级列表中，返回默认值
			return default
		# 返回有效的日志等级的大写形式
		return level.upper()
	
	def set_level(self, console="DEBUG", text="DEBUG"):
		"""
		设置显示等级，当实际等级低于设置等级的时候将不会显示/写入。
		
		:param console: 设置控制台显示的最低等级，可选值为 "DEBUG"、"INFO"、"WARNING"、"ERROR"。
						默认值为 "DEBUG"。
		:param text: 设置文本记录的最低等级，可选值为 "DEBUG"、"INFO"、"WARNING"、"ERROR"。
						默认值为 "DEBUG"。
		:return: 无返回值。
		"""	
		# 验证并设置日志等级，确保输入的等级有效
		console_level = self.validate_level(console)
		text_level = self.validate_level(text)
	
		try:
			# 根据验证后的等级从等级字典中获取对应的值，并设置控制台和文本记录的最低等级
			self.level_console = self.level_dic[console_level]
			self.level_text = self.level_dic[text_level]
		except KeyError as e:
			# 如果等级字典中缺少必要的键，则抛出异常
			raise ValueError(f"日志等级字典中缺少必要的键: {e}")
	
	def fun_info(self, info):
		"""
		获取function信息。
		
		:param info: list，包含文件名、行号、模块名等信息的列表。
						- info[0]: 文件名（str）
						- info[1]: 行号（int 或 str）
						- info[2]: 模块名（str）
		:return: 无返回值。该方法主要用于解析并设置类实例的属性。
		"""
		try:
			# 输入校验，确保 info 至少包含三个元素
			if len(info) < 3:
				raise ValueError("参数 info 的长度不足，至少需要包含三个元素")

			# 提取信息并赋值给实例属性
			self.line_ = info[1]  # 设置行号
			self.module_name = info[2]  # 设置模块名
			filename = info[0]  # 获取文件名

			# 调用内部方法处理文件名
			filename = self._process_filename(filename)

			# 将处理后的文件名赋值给实例属性
			self.filename = filename

		except (IndexError, AttributeError, ValueError) as e:
			# 捕获并处理异常，确保即使出错，属性也有默认值
			print(f"处理 info 时发生错误: {e}")
			self.filename = None
	
	
	def _process_filename(self, filename):
		"""
		处理文件名，提取文件路径的最后一部分。

		:param filename: 原始文件名或路径，可以是字符串或其他可转换为字符串的对象。
		:return: 处理后的文件名，返回路径中的最后一部分。
		"""
		# 将文件名转换为字符串并提取路径的最后一部分（适用于 Unix/Linux 系统）
		filename = str(filename).split('/')[-1]

		# 如果当前运行环境为 Windows 系统，进一步处理路径以适配 Windows 的路径分隔符
		if platform.system().lower() == 'windows':
			filename = os.path.split(filename)[1]

		return filename

	def _create_msg(self, msg, level='DEBUG'):
		"""
		创建信息字符串，根据类的属性格式化日志消息。

		:param msg: 需要记录的信息内容，类型为字符串。
		:param level: 信息的日志级别，默认值为 'DEBUG'，类型为字符串。
		:return: 无返回值，生成的消息存储在实例变量 self.msg1 中。
		"""
		try:
			# 尝试从 self.date 中分割日期和时间，捕获可能的异常
			date_, time_ = self.date.split(' ')
		except (AttributeError, ValueError):
			# 如果 self.date 不存在或格式不正确，将日期和时间设置为空字符串
			date_, time_ = '', ''

		# 初始化消息部分列表，用于存储需要拼接的字符串
		msg_parts = []
		if self.format_date:
			# 如果需要格式化日期，添加日期部分
			msg_parts.append(date_)
		if self.format_time:
			# 如果需要格式化时间，添加时间部分
			msg_parts.append(time_)
		if self.format_filename:
			# 如果需要格式化文件名，添加文件名部分
			msg_parts.append(self.filename)
		if self.format_line:
			# 如果需要格式化行号，添加行号部分
			msg_parts.append(f"line: {self.line_}")
		if self.caller_class is not None and self.format_class:
			# 如果存在调用类且需要格式化类名，添加类名部分
			msg_parts.append(f"Class: {self.caller_class}")
		if self.fun_name != '<module>' and self.format_fun:
			# 如果函数名不是默认模块名且需要格式化函数名，添加函数名部分
			msg_parts.append(f"Function: {self.fun_name}")
		if self.format_level:
			# 如果需要格式化日志级别，添加日志级别和消息部分
			msg_parts.append(f"{level} : {msg}")

		# 使用 ''.join() 方法高效拼接所有消息部分，生成最终的消息字符串
		self.msg1 = ' '.join(msg_parts)

	def _wr(self):
		"""
		写入日志信息到文本日志文件的辅助方法。

		该方法根据 `self.txt_mode` 的状态决定是否将 `self.msg1` 写入到 `self.txt_wr` 中。
		如果写入过程中发生异常，会捕获并记录错误日志。

		参数:
			无

		返回值:
			无

		可能抛出的异常:
			AttributeError: 如果 `self.txt_wr` 缺少 `write` 方法。
			ValueError: 如果 `self.txt_wr` 和 `self.msg1` 均未初始化（被注释掉的逻辑）。
			IOError: 如果在文件操作过程中发生 I/O 错误。
		"""

		try:
			# 如果开启了文本日志模式
			if self.txt_mode:
				# 确保 `self.txt_wr` 是一个有效的文件对象，并具有 `write` 方法
				if hasattr(self.txt_wr, 'write'):
					# 将消息写入文件，并添加换行符
					self.txt_wr.write(self.msg1)
					self.txt_wr.write("\n")
				else:
					# 如果 `self.txt_wr` 不支持写操作，抛出异常
					raise AttributeError("'txt_wr' does not have a 'write' method.")
		except IOError as io_err:
			# 捕获文件操作相关的异常，并记录错误日志
			self._log_error(f"IOError occurred while writing to file: {str(io_err)}")
		except Exception as e:
			# 捕获其他未预期的异常，并记录错误日志
			self._log_error(f"Unexpected error occurred: {str(e)}")
	
	def _log_error(self, message):
		"""
		记录错误信息到日志系统。

		参数:
			message (str): 需要记录的错误信息。

		返回值:
			无返回值。该函数仅用于输出错误信息到日志系统。
		"""
		# 假设有一个日志系统，将错误信息记录到日志中
		print(self.Red + message + self.RESET_ALL)

	def _arg(self, arg):
		"""
		解析参数并将其拼接为字符串。

		:param arg: 可迭代对象，包含需要解析的参数。每个元素会被转换为字符串后拼接。
		:return: 拼接后的字符串，所有元素按顺序连接成一个整体。
		:raises ValueError: 如果输入参数不是可迭代对象，则抛出异常，并附带错误详情。
		"""
		try:
			# 使用 str.join() 提高字符串拼接效率，避免频繁创建中间字符串对象
			return ''.join(str(i) for i in arg)
		except TypeError as e:
			# 捕获并处理非可迭代对象的错误，确保函数调用者能够明确问题原因
			raise ValueError(f"输入参数必须是可迭代对象，错误详情: {e}")

	def _get_time(self):
		"""
		获取当前时间并格式化为字符串形式。

		该函数将当前时间（精确到秒）存储在实例属性 `self.date` 中。
		时间格式为 "YYYY-MM-DD HH:MM:SS"，通过去除微秒部分实现。

		参数:
			无

		返回值:
			无
		"""
		# 将当前时间转换为字符串并去除微秒部分
		self.date = str(datetime.now()).split('.')[0]

	def info(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		try:
			# 获取调用方法所在的类名和方法名
			caller_frame = inspect.currentframe().f_back
			caller_instance = caller_frame.f_locals.get('self', None)
			self.caller_class = caller_instance.__class__.__name__ if caller_instance else 'UnknownClass'
			self.caller_method = caller_frame.f_code.co_name
			self.fun_name = self.caller_method

			# 获取调用栈信息
			fun_info = inspect.getframeinfo(caller_frame)
			self.fun_info(info=fun_info)

			self._get_time()

			# 处理消息内容
			msg = str(msg)
			if arg:
				msg += ''.join(str(item) for item in self._arg(arg=arg))
			if kwarg:
				msg += ''.join(str(item) for item in self._arg(arg=kwarg))

			self._create_msg(msg=msg, level="INFO")

			# 构造输出信息
			mess = f"{self.Greet}{self.msg1}{self.RESET_ALL}"
			if self.fileinfo and self.txt_mode:
				mess = f"{self.Greet}{self.file_name} <<-- {self.msg1}{self.RESET_ALL}"

			if self.level_console <= 1:
				print(mess)
			if self.level_text <= 1:
				self._wr()
		except Exception as e:
			print(f"{self.Red}Logger error: {str(e)}{self.RESET_ALL}")

	def debug(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		# 使用更高效的方式获取调用信息
		caller_frame = inspect.currentframe().f_back
		caller_info = inspect.getframeinfo(caller_frame)
		
		# 安全获取类名
		caller_self = caller_frame.f_locals.get('self', None)
		caller_class = getattr(caller_self, '__class__', type(None)).__name__
		
		# 使用局部变量替代实例属性
		fun_name = caller_frame.f_code.co_name
		file_info = self.fun_info(info=caller_info)  # 假设返回需要的信息
		
		# 合并参数处理
		msg_parts = [str(msg)]
		if arg:
			msg_parts.append(str(self._arg(arg=arg)))
		if kwarg:
			msg_parts.append(str(self._arg(arg=kwarg)))
		full_msg = ''.join(msg_parts)
		
		# 构建显示信息
		self._get_time()
		self._create_msg(msg=full_msg)
		
		# 优化字符串构建
		base_message = f"{self.Blue}{self.msg1}{self.RESET_ALL}"
		mess = base_message
		if self.fileinfo and self.txt_mode:
			mess = f"{self.Blue}{self.file_name} <<-- {self.msg1}{self.RESET_ALL}"
		
		# 输出处理
		if self.level_console == 0:
			print(mess)
		if self.level_text <= 0:
			self._wr()

	def warning(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		# 优化后的调用链获取逻辑
		caller_frame = inspect.currentframe().f_back
		caller_instance = caller_frame.f_locals.get('self', None)
		
		# 安全获取类名
		caller_class = caller_instance.__class__.__name__ if caller_instance else 'UnknownClass'
		caller_method = caller_frame.f_code.co_name
		
		# 合并参数处理
		params = []
		if arg:
			params.append(self._arg(arg=arg))
		if kwarg:
			params.append(self._arg(arg=kwarg))
		msg = str(msg) + ''.join(params)
		
		# 使用格式化字符串提升可读性
		color_prefix = self.Yellow
		color_suffix = self.RESET_ALL
		
		base_message = f"{color_prefix}{self.msg1}{color_suffix}"
		if self.fileinfo and self.txt_mode:
			base_message = f"{color_prefix}{self.file_name} <<-- {self.msg1}{color_suffix}"
		
		# 统一消息生成逻辑
		self._create_msg(msg=msg, level="WARNING")
		
		# 输出控制
		if self.level_console <= 2:
			print(base_message)
		if self.level_text <= 2:
			self._wr()

	def error(self, msg, *arg, **kwarg):
		"""
		打印信息
		:param msg: 打印内容
		:return:
		"""
		# 获取调用方法所在的类名和方法名
		self.caller_frame = inspect.stack()[1]
		self.caller_class = self.caller_frame[0].f_locals.get('self', None).__class__.__name__
		self.caller_method = self.caller_frame[3]
		self.fun_name = self.caller_frame[3]
		fun_info = inspect.getframeinfo(inspect.currentframe().f_back)
		self.fun_info(info=fun_info)
		self._get_time()
		if arg:
			msg = str(msg) + str(self._arg(arg=arg))
		if kwarg:
			msg = str(msg) + str(self._arg(arg=kwarg))
		self._create_msg(msg=msg, level="ERROR")
		mess = str(self.Red + self.msg1 + self.RESET_ALL)
		if self.fileinfo and self.txt_mode:
			mess = str(self.Red + str(self.file_name) + ' <<-- ' + self.msg1 + self.RESET_ALL)
		if self.level_console <= 3:
			print(mess)
		if self.level_text <= 3:
			self._wr()


logger = ColorLogger()
if __name__ == "__main__":
	log = ColorLogger(fileinfo=True, basename=True, txt=False)
	log.info(msg='1', x="23")
	log.error('2', '22', '222')
	log.set_level(console="INFO")
	log.debug('3', '21')
	log.warning('4', '20', 22)
