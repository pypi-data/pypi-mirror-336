#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WavX LOGO模块

提供显示WavX LOGO的功能
"""

def print_logo(with_version=True):
    """
    打印WavX的ASCII艺术LOGO
    
    参数:
        with_version: 是否显示版本信息
    """
    from .. import __version__
    
    logo = """
 _       __          ____  __
| |     / /___ __   / __ \/ /
| | /| / / __ `/ | / / / / / 
| |/ |/ / /_/ /| |/ /_/ /_/  
|__/|__/\__,_/ |___\____(_)  
    """
    
    if with_version:
        from .. import __version__
        logo += f"\n      v{__version__}\n"
    
    print(logo)

def print_install_message():
    """
    打印安装完成后的欢迎消息和LOGO
    """
    print_logo()
    print("文档: https://github.com/chord-chord/wavx")
    print("使用 'wavx --help' 查看命令行工具的使用方法")
