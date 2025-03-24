#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
安装脚本工具

用于pip安装过程中的自定义处理
"""

def post_install():
    """
    安装后处理，显示欢迎信息和LOGO
    """
    try:
        from wavx.utils.logo import print_install_message
        print_install_message()
    except ImportError:
        # 如果无法导入WavX，则使用一个简单的消息
        print("文档: https://github.com/JiangYain/WavX")
        print("使用 'wavx --help' 查看命令行工具的使用方法")

if __name__ == "__main__":
    post_install() 