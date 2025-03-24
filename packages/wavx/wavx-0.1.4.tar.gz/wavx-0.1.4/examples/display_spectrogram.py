#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WavX 频谱图示例

演示如何使用WavX生成和显示音频文件的频谱图
"""

import os
import sys
import argparse
import matplotlib.pyplot as plt

# 添加项目根目录到Python路径，以便能够导入wavx包
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import wavx


def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='WavX 频谱图示例')
    parser.add_argument('audio_file', help='音频文件路径')
    parser.add_argument('--channel', '-c', type=int, default=0, help='分析通道 (0=左声道, 1=右声道)')
    parser.add_argument('--freq-limit', '-f', type=int, default=8000, help='频率上限 (Hz)')
    parser.add_argument('--linear', action='store_true', help='使用线性刻度而不是对数刻度')
    parser.add_argument('--save', '-s', help='保存频谱图的文件路径 (例如: spectrogram.png)')
    args = parser.parse_args()

    # 基本方法：直接分析并显示频谱图
    print("方法1: 使用一体化函数显示频谱图")
    wavx.analysis.spectrogram.display_spectrogram(
        audio_file=args.audio_file,
        channel=args.channel,
        use_log_scale=not args.linear,
        freq_limit=args.freq_limit,
        save_path=args.save
    )

    # 高级方法：分步处理
    print("\n方法2: 分步处理频谱图")
    # 1. 分析频谱图
    spec_data = wavx.analysis.spectrogram.analyze_spectrogram(
        audio_file=args.audio_file,
        channel=args.channel
    )
    
    # 2. 打印频谱图信息
    wavx.analysis.spectrogram.print_spectrogram_info(spec_data)
    
    # 3. 绘制频谱图
    fig = wavx.analysis.spectrogram.plot_spectrogram(
        spec_data=spec_data,
        use_log_scale=not args.linear,
        freq_limit=args.freq_limit,
        figsize=(10, 6),
        save_path=None  # 这里不保存，只显示
    )
    
    # 4. 添加自定义绘图元素
    plt.axhline(y=1000, color='r', linestyle='--', label='1kHz参考线')
    plt.legend()
    
    # 5. 显示修改后的图像
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main() 