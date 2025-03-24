# WavX

[English](#wavx) | [中文](#wavx-1)

WavX is a Python library for audio analysis and processing, providing a simple yet powerful API for handling various audio-related tasks.

## Features

- Audio file analysis, including amplitude, loudness, and acoustic parameter measurement
- Audio processing, including RMS level normalization
- Modular design, easy to extend
- Clean and intuitive API interface

## Installation

```bash
pip install wavx
```

## Quick Start

### Analyze audio file amplitude information

```python
import wavx

# Analyze audio file and get amplitude information
amplitude_info = wavx.analysis.amplitude.analyze_amplitude("your_audio_file.wav")

# Print all amplitude information
wavx.analysis.amplitude.print_amplitude_info(amplitude_info)

# Or get specific information
print(f"Peak amplitude: {amplitude_info['peak_amplitude']} dB")
print(f"Total RMS amplitude: {amplitude_info['total_rms_amplitude']} dB")
```

### Generate and display audio waveform

```python
import wavx

# Simple way: Display waveform with one function call
wavx.analysis.waveform.display_waveform("your_audio_file.wav")

# Advanced way: Step by step for more control
# 1. Analyze waveform data
waveform_data = wavx.analysis.waveform.analyze_waveform(
    audio_file="your_audio_file.wav",
    channel=0  # 0=left channel, 1=right channel
)

# 2. Print waveform information
wavx.analysis.waveform.print_waveform_info(waveform_data)

# 3. Plot waveform with custom settings
import matplotlib.pyplot as plt
fig = wavx.analysis.waveform.plot_waveform(
    waveform_data=waveform_data,
    figsize=(12, 4),     # figure size
    save_path="waveform.png",  # save to file
    color="Aqua Gray"    # use predefined color scheme
)
plt.show()

# Available colors:
# - "Aqua Gray": "#7FBFBF"
# - "Muted Purple": "#9E91B7"
# - "Olive Green": "#9DB17C" (default)
# - "Soft Coral": "#E1A193"
# - "Slate Blue": "#7A8B99"
# - "Dusty Rose": "#C2A9A1"
```

### Generate and display audio spectrogram

```python
import wavx

# Simple way: Display spectrogram with one function call
wavx.analysis.spectrogram.display_spectrogram("your_audio_file.wav")

# Advanced way: Step by step for more control
# 1. Analyze spectrogram data
spec_data = wavx.analysis.spectrogram.analyze_spectrogram(
    audio_file="your_audio_file.wav",
    channel=0,  # 0=left channel, 1=right channel
    window_size=1024,  # window size
    overlap=0.75  # 75% window overlap
)

# 2. Print spectrogram information
wavx.analysis.spectrogram.print_spectrogram_info(spec_data)

# 3. Plot spectrogram with custom settings
import matplotlib.pyplot as plt
fig = wavx.analysis.spectrogram.plot_spectrogram(
    spec_data=spec_data,
    use_log_scale=True,  # use dB scale
    freq_limit=8000,     # limit to 8kHz
    figsize=(10, 3.5),   # figure size
    save_path="spectrogram.png"  # save to file
)
plt.show()
```

### Normalize audio file to target RMS level

```python
import wavx

# Normalize audio file to -20 dB FS
result = wavx.processing.normalization.normalize_to_target(
    input_file="input.wav",
    output_file="output.wav",
    target_rms_db=-20.0,
    reference_type="square"  # or "sine"
)

# Print normalization information
wavx.processing.normalization.print_normalization_info(result)
```

## Project Structure

```
wavx/
├── docs/
│   ├── amplitude/
│   │   └── amplitude_analysis.md  # Amplitude analysis documentation
│   ├── analysis/
│   │   └── spectrogram.md         # Spectrogram analysis documentation
│   └── processing/
│       └── normalization.md       # RMS normalization documentation
├── examples/
│   ├── analyze_audio.py           # Example of audio analysis
│   ├── display_spectrogram.py     # Example of spectrogram visualization
│   └── normalize_audio.py         # Example of audio normalization
├── wavx/
│   ├── __init__.py                # Package initialization
│   ├── cli.py                     # Command line interface
│   ├── analysis/
│   │   ├── __init__.py            # Analysis module initialization
│   │   ├── amplitude.py           # Amplitude analysis functionality
│   │   └── spectrogram.py         # Spectrogram analysis functionality
│   ├── processing/
│   │   ├── __init__.py            # Processing module initialization
│   │   └── normalization.py       # RMS normalization functionality
│   ├── tests/
│   │   ├── __init__.py            # Tests initialization
│   │   ├── test_amplitude.py      # Amplitude analysis tests
│   │   └── test_normalization.py  # Normalization tests
│   └── utils/
│       └── __init__.py            # Utilities module initialization
├── README.md                      # English documentation
├── README_zh.md                   # Chinese documentation
├── requirements.txt               # Project dependencies
└── setup.py                       # Package installation config
```

## Command Line Usage

After installation, you can use WavX from the command line:

```bash
# Basic amplitude analysis
wavx amplitude path/to/audio.wav

# Generate and display waveform
wavx waveform path/to/audio.wav

# Waveform with custom parameters
wavx waveform path/to/audio.wav --channel 1 --save output.png

# Generate and display spectrogram
wavx spectrogram path/to/audio.wav

# Spectrogram with custom parameters
wavx spectrogram path/to/audio.wav --channel 1 --freq-limit 5000 --save output.png

# RMS normalization
wavx normalize input.wav output.wav --target -18.0

# With custom reference signal
wavx normalize input.wav output.wav --reference sine --freq 500
```

## Future Extensions

The modular design allows easy extensions:

1. **More Analysis Functions**:
   - Spectrum analysis
   - Harmonic analysis
   - Reverb and spatial analysis

2. **More Audio Processing**:
   - Equalization
   - Noise reduction
   - Dynamic range compression
   - Resampling and format conversion

3. **Visualization**:
   - Waveform display
   - Spectrogram
   - Loudness/RMS history

## Release Notes

- v0.1.8 (2025-03-24): Version control upgrade
- v0.1.8 (2025-03-26): Added waveform color schemes and optimized spectrogram display
- v0.1.7 (2025-03-25): Enhanced waveform CLI support and documentation
- v0.1.6 (2025-03-24): Version control upgrade
- v0.1.5 (2025-03-22): Added waveform visualization functionality
- v0.1.4 (2025-03-21): Added spectrogram analysis and visualization
- v0.1.3 (2025-03-20): Added WAVX LOGO display after pip install
- v0.1.2 (2025-03-20): Added RMS normalization functionality
- v0.1.1 (2025-03-20): Added docs directory and bilingual README files
- v0.1.0 (2025-03-20): Initial release with amplitude analysis functionality

## Contributing

Contributions to the code, questions, or suggestions are welcome!

## License

MIT License

---

# WavX

WavX 是一个用于音频分析和处理的Python库，提供简单而强大的API来处理各种音频相关任务。

## 特性

- 音频文件分析，包括振幅、响度和声学参数测量
- 音频处理，包括RMS电平标准化
- 模块化设计，易于扩展
- 简洁直观的API接口

## 安装

```bash
pip install wavx
```

## 快速开始

### 分析音频文件振幅信息

```python
import wavx

# 分析音频文件并获取振幅信息
amplitude_info = wavx.analysis.amplitude.analyze_amplitude("your_audio_file.wav")

# 打印所有振幅信息
wavx.analysis.amplitude.print_amplitude_info(amplitude_info)

# 或者获取特定信息
print(f"峰值幅度: {amplitude_info['peak_amplitude']} dB")
print(f"总计 RMS 振幅: {amplitude_info['total_rms_amplitude']} dB")
```

### 生成并显示音频波形图

```python
import wavx

# 简单方式：一步完成波形图显示
wavx.analysis.waveform.display_waveform("your_audio_file.wav")

# 高级方式：分步骤进行，获得更多控制
# 1. 分析波形数据
waveform_data = wavx.analysis.waveform.analyze_waveform(
    audio_file="your_audio_file.wav",
    channel=0  # 0=左声道, 1=右声道
)

# 2. 打印波形信息
wavx.analysis.waveform.print_waveform_info(waveform_data)

# 3. 使用自定义设置绘制波形图
import matplotlib.pyplot as plt
fig = wavx.analysis.waveform.plot_waveform(
    waveform_data=waveform_data,
    figsize=(12, 4),     # 图形大小
    save_path="waveform.png",  # 保存到文件
    color="Aqua Gray"    # 使用预定义配色
)
plt.show()

# 可用颜色：
# - "Aqua Gray": "#7FBFBF"
# - "Muted Purple": "#9E91B7"
# - "Olive Green": "#9DB17C" (默认)
# - "Soft Coral": "#E1A193"
# - "Slate Blue": "#7A8B99"
# - "Dusty Rose": "#C2A9A1"
```

### 生成并显示音频频谱图

```python
import wavx

# 简单方式：一步完成频谱图显示
wavx.analysis.spectrogram.display_spectrogram("your_audio_file.wav")

# 高级方式：分步骤进行，获得更多控制
# 1. 分析频谱图数据
spec_data = wavx.analysis.spectrogram.analyze_spectrogram(
    audio_file="your_audio_file.wav",
    channel=0,  # 0=左声道, 1=右声道
    window_size=1024,  # 窗口大小
    overlap=0.75  # 75%窗口重叠
)

# 2. 打印频谱图信息
wavx.analysis.spectrogram.print_spectrogram_info(spec_data)

# 3. 使用自定义设置绘制频谱图
import matplotlib.pyplot as plt
fig = wavx.analysis.spectrogram.plot_spectrogram(
    spec_data=spec_data,
    use_log_scale=True,  # 使用分贝刻度
    freq_limit=8000,     # 限制到8kHz
    figsize=(10, 3.5),   # 图形大小
    save_path="spectrogram.png"  # 保存到文件
)
plt.show()
```

### 将音频文件标准化到目标RMS电平

```python
import wavx

# 将音频文件标准化到 -20 dB FS
result = wavx.processing.normalization.normalize_to_target(
    input_file="input.wav",
    output_file="output.wav",
    target_rms_db=-20.0,
    reference_type="square"  # 或 "sine"
)

# 打印标准化信息
wavx.processing.normalization.print_normalization_info(result)
```

## 命令行使用

安装后，可以从命令行使用WavX：

```bash
# 基本振幅分析
wavx amplitude path/to/audio.wav

# 生成并显示波形图
wavx waveform path/to/audio.wav

# 带自定义参数的波形图
wavx waveform path/to/audio.wav --channel 1 --save output.png

# 生成并显示频谱图
wavx spectrogram path/to/audio.wav

# 带自定义参数的频谱图
wavx spectrogram path/to/audio.wav --channel 1 --freq-limit 5000 --save output.png

# RMS标准化
wavx normalize input.wav output.wav --target -18.0

# 使用自定义参考信号
wavx normalize input.wav output.wav --reference sine --freq 500
```

## 发布说明

- v0.1.8 (2025-03-26): 添加波形图配色方案和优化频谱图显示
- v0.1.7 (2025-03-25): 增强波形图命令行支持和文档
- v0.1.6 (2025-03-24): 版本控制升级
- v0.1.5 (2025-03-22): 添加波形图可视化功能
- v0.1.4 (2025-03-21): 添加频谱图分析和可视化功能
- v0.1.3 (2025-03-20): 添加pip安装后显示WAVX LOGO功能
- v0.1.2 (2025-03-20): 添加RMS标准化功能
- v0.1.1 (2025-03-20): 添加文档目录和双语README文件
- v0.1.0 (2025-03-20): 初始版本，包含振幅分析功能

## 贡献

欢迎对代码贡献、提问或提出改进建议！

## 许可证

MIT 许可证 