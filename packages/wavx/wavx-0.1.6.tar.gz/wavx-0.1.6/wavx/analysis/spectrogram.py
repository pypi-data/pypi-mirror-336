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
from matplotlib import font_manager as fm

# 添加Times New Roman字体设置
def set_plot_style():
    """
    设置绘图样式，使用Times New Roman字体
    """
    # 设置全局字体为Times New Roman
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['mathtext.fontset'] = 'stix'  # 数学公式字体
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号


def analyze_spectrogram(audio_file: str, 
                        channel: int = 0, 
                        window_size: Optional[int] = None,
                        overlap: float = 0.5) -> Dict[str, Any]:
    """
    分析音频文件的频谱图

    参数:
        audio_file: 音频文件路径
        channel: 要分析的通道 (0=左, 1=右)
        window_size: 窗口大小 (None 表示使用默认值)
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

    # 使用默认窗口参数
    if window_size is None:
        window_size = 256  # 使用scipy.signal.spectrogram的默认值

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
                     save_path: Optional[str] = None,
                     vmin: float = -100,  # 添加最小值参数
                     vmax: float = -50    # 添加最大值参数
                     ) -> plt.Figure:
    """
    Plot spectrogram of audio data

    Args:
        spec_data: Spectrogram data from analyze_spectrogram
        use_log_scale: Whether to use log scale display
        freq_limit: Frequency limit (Hz), None for full range
        figsize: Figure size
        save_path: If provided, save figure to this path
        vmin: Minimum value for color scale (dB)
        vmax: Maximum value for color scale (dB)

    Returns:
        matplotlib figure object
    """
    frequencies = spec_data['frequencies']
    times = spec_data['times']
    Sxx = spec_data['spectrogram']
    
    # 设置绘图样式
    set_plot_style()
    
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
        colorbar_label = 'Intensity [dB]'  # 改为 Intensity
    else:
        display_data = Sxx
        colorbar_label = 'Intensity'
    
    # 绘制频谱图，添加颜色范围控制
    plt.pcolormesh(times, frequencies, display_data, 
                  shading='gouraud',
                  vmin=vmin,
                  vmax=vmax)
    plt.colorbar(label=colorbar_label)
    
    # 设置标题和标签
    audio_file = spec_data['audio_file'].split("/")[-1]
    plt.title(f"Spectrogram: {audio_file}", pad=10)
    plt.xlabel("Time [s]")
    plt.ylabel("Frequency [Hz]")
    
    # 优化布局
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
    print(f"Audio file: {spec_data['audio_file']}")
    print(f"Sample rate: {spec_data['sample_rate']} Hz")
    print(f"Data length: {len(spec_data['data'])} samples")
    print(f"Duration: {len(spec_data['data']) / spec_data['sample_rate']:.2f} seconds")
    print(f"Frequency resolution: {len(spec_data['frequencies'])} points")
    print(f"Time resolution: {len(spec_data['times'])} frames")
    print(f"Window size: {spec_data['window_size']} samples")
    print(f"Overlap ratio: {spec_data['overlap']:.2f}")


def display_spectrogram(audio_file: str, 
                        channel: int = 0,
                        window_size: Optional[int] = None,
                        overlap: float = 0.75,
                        use_log_scale: bool = True,
                        freq_limit: Optional[int] = None,
                        figsize: Tuple[int, int] = (12, 4),
                        save_path: Optional[str] = None) -> None:
    """
    Analyze and display spectrogram of audio file
    
    Args:
        audio_file: Path to audio file
        channel: Channel to analyze (0=left, 1=right)
        window_size: Window size (None for auto)
        overlap: Window overlap ratio (0.0-1.0)
        use_log_scale: Whether to use log scale display
        freq_limit: Frequency limit (Hz), None for full range
        figsize: Figure size
        save_path: If provided, save figure to this path
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