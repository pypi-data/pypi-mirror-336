#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WavX - 音频分析和处理工具库

WavX是一个模块化的音频处理库，提供各种声学分析和处理功能。
"""

__version__ = '0.1.4'
__author__ = 'Chord'

# 导入子模块
from . import analysis
from . import utils
from . import processing

# 设置日志
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

# 如果检测到是通过pip安装的，则在安装完成后显示LOGO
import os
import sys

def _is_pip_install():
    """检查是否是通过pip install命令安装"""
    return any(arg.startswith('install') for arg in sys.argv)

# 如果是通过pip install安装并且不是在setup.py的上下文中
if _is_pip_install() and 'setup.py' not in sys.argv[0].lower():
    try:
        # 尝试调用post_install函数
        import subprocess
        import atexit
        
        # 注册退出时调用wavx-welcome
        def _show_logo_on_exit():
            try:
                subprocess.call([sys.executable, '-m', 'scripts'])
            except:
                pass
        
        atexit.register(_show_logo_on_exit)
    except:
        pass
