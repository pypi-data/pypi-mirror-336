# -*- encoding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()
setuptools.setup(
	name="ColorInfo",
	version="2.2.1",
	author="坐公交也用券",
	author_email="liumou.site@qq.com",
	description="ColorInfo 是一个使用Python3编写的简单的彩色日志工具，拥有简单、友好的语法,采用纯原始功能实现,无需依赖任何第三方模块",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitee.com/liumou_site/ColorInfo",
	packages=["ColorInfo"],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",

	],
	# Py版本要求
	python_requires='>=3.0',
	# 依赖
	install_requires=[]
)
