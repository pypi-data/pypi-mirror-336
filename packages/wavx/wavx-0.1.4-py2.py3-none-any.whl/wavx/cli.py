#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WavX 命令行界面

提供命令行访问WavX库功能的入口点
"""

import argparse
import sys
from typing import List, Optional

from . import __version__
from .analysis import amplitude
from .analysis import spectrogram
from .processing import normalization
from .utils.logo import print_logo


def main(args: Optional[List[str]] = None) -> int:
    """
    命令行入口函数
    
    参数:
        args: 命令行参数列表。如果为None，则使用sys.argv
        
    返回:
        int: 退出码。0表示成功，非零表示错误
    """
    parser = argparse.ArgumentParser(
        description=f"WavX v{__version__} - 音频分析和处理工具库",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--version', action='version',
        version=f'WavX {__version__}'
    )
    
    # 创建子命令
    subparsers = parser.add_subparsers(dest='command', help='可用命令')
    
    # 振幅分析命令
    amplitude_parser = subparsers.add_parser('amplitude', help='分析音频文件的振幅信息')
    amplitude_parser.add_argument('audio_file', help='要分析的音频文件路径')
    amplitude_parser.add_argument('--window', type=float, default=50.0, help='RMS窗口大小(毫秒)')
    amplitude_parser.add_argument('--no-dc', action='store_false', dest='consider_dc', help='不考虑DC偏移')
    
    # 频谱图分析命令
    spectrogram_parser = subparsers.add_parser('spectrogram', help='分析并显示音频文件的频谱图')
    spectrogram_parser.add_argument('audio_file', help='要分析的音频文件路径')
    spectrogram_parser.add_argument('--channel', '-c', type=int, default=0, help='要分析的通道 (0=左, 1=右)')
    spectrogram_parser.add_argument('--window', '-w', type=int, help='窗口大小 (默认自动设置)')
    spectrogram_parser.add_argument('--overlap', '-o', type=float, default=0.75, help='窗口重叠比例 (0.0-1.0)')
    spectrogram_parser.add_argument('--linear', action='store_false', dest='log_scale', help='使用线性刻度而不是对数刻度')
    spectrogram_parser.add_argument('--freq-limit', '-f', type=int, help='频率上限 (Hz)')
    spectrogram_parser.add_argument('--save', '-s', help='保存频谱图的文件路径')
    
    # RMS标准化命令
    normalize_parser = subparsers.add_parser('normalize', help='将音频文件标准化到指定的RMS电平')
    normalize_parser.add_argument('input_file', help='输入音频文件路径')
    normalize_parser.add_argument('output_file', help='输出音频文件路径')
    normalize_parser.add_argument('--target', '-t', type=float, default=-20.0, help='目标RMS电平(dB FS)，默认为-20dB')
    normalize_parser.add_argument('--reference', '-r', choices=['square', 'sine'], default='square', 
                                 help='参考信号类型，可选"square"或"sine"，默认为"square"')
    normalize_parser.add_argument('--freq', '-f', type=float, default=1000.0, help='参考信号频率(Hz)，默认为1000Hz')
    normalize_parser.add_argument('--duration', '-d', type=float, default=1.0, help='参考信号持续时间(秒)，默认为1秒')
    
    # 解析参数
    parsed_args = parser.parse_args(args)
    
    # 如果没有提供命令，显示LOGO和帮助信息
    if not parsed_args.command:
        print_logo()
        parser.print_help()
        return 0
    
    # 处理命令
    if parsed_args.command == 'amplitude':
        try:
            # 分析音频文件
            print(f"分析音频文件: {parsed_args.audio_file}")
            print(f"RMS窗口大小: {parsed_args.window} ms")
            print(f"考虑DC偏移: {parsed_args.consider_dc}")
            print("正在分析...")
            
            # 调用分析函数
            info = amplitude.analyze_amplitude(
                parsed_args.audio_file,
                rms_window_ms=parsed_args.window,
                consider_dc=parsed_args.consider_dc
            )
            
            # 打印结果
            amplitude.print_amplitude_info(info)
            
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            return 1
    
    elif parsed_args.command == 'spectrogram':
        try:
            # 分析并显示频谱图
            print(f"分析音频文件: {parsed_args.audio_file}")
            print(f"通道: {parsed_args.channel}")
            print(f"使用对数刻度: {parsed_args.log_scale}")
            if parsed_args.freq_limit:
                print(f"频率上限: {parsed_args.freq_limit} Hz")
            if parsed_args.save:
                print(f"保存到: {parsed_args.save}")
            print("正在生成频谱图...")
            
            # 调用频谱图函数
            spectrogram.display_spectrogram(
                audio_file=parsed_args.audio_file,
                channel=parsed_args.channel,
                window_size=parsed_args.window,
                overlap=parsed_args.overlap,
                use_log_scale=parsed_args.log_scale,
                freq_limit=parsed_args.freq_limit,
                save_path=parsed_args.save
            )
            
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            return 1
    
    elif parsed_args.command == 'normalize':
        try:
            # 标准化音频文件
            print(f"正在将音频文件 '{parsed_args.input_file}' 标准化到 {parsed_args.target} dB FS...")
            print(f"使用参考信号: {parsed_args.reference}波 {parsed_args.freq} Hz")
            print(f"输出文件: {parsed_args.output_file}")
            
            # 调用标准化函数
            info = normalization.normalize_to_target(
                input_file=parsed_args.input_file,
                output_file=parsed_args.output_file,
                target_rms_db=parsed_args.target,
                reference_type=parsed_args.reference,
                reference_duration=parsed_args.duration,
                reference_freq=parsed_args.freq
            )
            
            # 打印结果
            normalization.print_normalization_info(info)
            
        except Exception as e:
            print(f"错误: {e}", file=sys.stderr)
            return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())