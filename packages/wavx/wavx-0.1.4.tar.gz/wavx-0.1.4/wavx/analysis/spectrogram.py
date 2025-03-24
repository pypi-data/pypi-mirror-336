#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
频谱图分析模块

提供音频文件频谱图分析和显示功能
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal
import soundfile as sf
from typing import Dict, Any, Tuple, Optional


def analyze_spectrogram(audio_file: str, 
                        channel: int = 0, 
                        window_size: Optional[int] = None,
                        overlap: float = 0.75) -> Dict[str, Any]:
    """
    分析音频文件的频谱图

    参数:
        audio_file: 音频文件路径
        channel: 要分析的通道 (0=左, 1=右)
        window_size: 窗口大小 (None 表示自动)
        overlap: 窗口重叠比例 (0.0-1.0)

    返回:
        包含频谱图数据的字典
    """
    # 读取音频文件
    try:
        sample_rate, data = wavfile.read(audio_file)
        # 检查文件类型，如果不是WAV，使用soundfile
        if data.dtype == 'float32' or data.dtype == 'float64':
            data = np.iinfo(np.int16).max * data
    except:
        # 如果wavfile无法读取，尝试使用soundfile
        data, sample_rate = sf.read(audio_file)
        # 将数据归一化到16位整数范围
        if data.dtype == 'float32' or data.dtype == 'float64':
            data = np.iinfo(np.int16).max * data

    # 如果是立体声，取指定的通道
    if data.ndim > 1:
        if channel >= data.shape[1]:
            channel = 0  # 如果指定的通道不可用，默认使用第一个
        data = data[:, channel]

    # 设置默认窗口大小
    if window_size is None:
        window_size = int(sample_rate * 0.025)  # 默认25ms窗口

    # 计算频谱
    frequencies, times, Sxx = signal.spectrogram(
        data, 
        fs=sample_rate,
        nperseg=window_size,
        noverlap=int(window_size * overlap)
    )

    return {
        'audio_file': audio_file,
        'sample_rate': sample_rate,
        'data': data,
        'frequencies': frequencies,
        'times': times,
        'spectrogram': Sxx,
        'channel': channel,
        'window_size': window_size,
        'overlap': overlap
    }


def plot_spectrogram(spec_data: Dict[str, Any], 
                     use_log_scale: bool = True,
                     freq_limit: Optional[int] = None,
                     figsize: Tuple[int, int] = (12, 4),
                     save_path: Optional[str] = None) -> plt.Figure:
    """
    绘制音频的频谱图

    参数:
        spec_data: 从analyze_spectrogram获取的频谱图数据
        use_log_scale: 是否使用对数刻度显示
        freq_limit: 频率上限 (Hz)，None表示显示全部
        figsize: 图像大小
        save_path: 如果提供，保存图像到此路径

    返回:
        matplotlib图形对象
    """
    frequencies = spec_data['frequencies']
    times = spec_data['times']
    Sxx = spec_data['spectrogram']
    
    # 创建图形
    fig = plt.figure(figsize=figsize)
    
    # 限制频率范围
    if freq_limit is not None and freq_limit > 0:
        freq_mask = frequencies <= freq_limit
        frequencies = frequencies[freq_mask]
        Sxx = Sxx[freq_mask, :]
    
    # 计算显示数据
    if use_log_scale:
        # 加入1e-10防止log(0)
        display_data = 10 * np.log10(Sxx + 1e-10)
        colorbar_label = '强度 [dB]'
    else:
        display_data = Sxx
        colorbar_label = '强度'
    
    # 绘制频谱图
    plt.pcolormesh(times, frequencies, display_data, shading='gouraud')
    plt.colorbar(label=colorbar_label)
    
    # 设置标题和标签
    audio_file = spec_data['audio_file'].split("/")[-1]
    plt.title(f"频谱图: {audio_file}")
    plt.xlabel("时间 [秒]")
    plt.ylabel("频率 [Hz]")
    plt.tight_layout()
    
    # 保存图像
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return fig


def print_spectrogram_info(spec_data: Dict[str, Any]) -> None:
    """
    打印频谱图分析信息

    参数:
        spec_data: 从analyze_spectrogram获取的频谱图数据
    """
    print(f"音频文件: {spec_data['audio_file']}")
    print(f"采样率: {spec_data['sample_rate']} Hz")
    print(f"数据长度: {len(spec_data['data'])} 样本")
    print(f"持续时间: {len(spec_data['data']) / spec_data['sample_rate']:.2f} 秒")
    print(f"频率分辨率: {len(spec_data['frequencies'])} 点")
    print(f"时间分辨率: {len(spec_data['times'])} 帧")
    print(f"窗口大小: {spec_data['window_size']} 样本")
    print(f"重叠比例: {spec_data['overlap']:.2f}")


def display_spectrogram(audio_file: str, 
                        channel: int = 0,
                        window_size: Optional[int] = None,
                        overlap: float = 0.75,
                        use_log_scale: bool = True,
                        freq_limit: Optional[int] = None,
                        figsize: Tuple[int, int] = (12, 4),
                        save_path: Optional[str] = None) -> None:
    """
    分析并显示音频文件的频谱图
    
    参数:
        audio_file: 音频文件路径
        channel: 要分析的通道 (0=左, 1=右)
        window_size: 窗口大小 (None 表示自动)
        overlap: 窗口重叠比例 (0.0-1.0)
        use_log_scale: 是否使用对数刻度显示
        freq_limit: 频率上限 (Hz)，None表示显示全部
        figsize: 图像大小
        save_path: 如果提供，保存图像到此路径
    """
    # 分析频谱图
    spec_data = analyze_spectrogram(
        audio_file=audio_file,
        channel=channel,
        window_size=window_size,
        overlap=overlap
    )
    
    # 打印信息
    print_spectrogram_info(spec_data)
    
    # 绘制并显示频谱图
    fig = plot_spectrogram(
        spec_data=spec_data,
        use_log_scale=use_log_scale,
        freq_limit=freq_limit,
        figsize=figsize,
        save_path=save_path
    )
    
    plt.show()
    
    return spec_data 