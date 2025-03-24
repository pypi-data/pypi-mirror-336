# 音频频谱图分析 / Audio Spectrogram Analysis

WavX提供了功能强大的频谱图分析工具，能够可视化音频文件的时频特性。
WavX provides powerful spectrogram analysis tools to visualize the time-frequency characteristics of audio files.

## 基本用法 / Basic Usage

```python
import wavx

# 分析并显示频谱图 / Analyze and display spectrogram
wavx.analysis.spectrogram.display_spectrogram("your_audio_file.wav")
```

## 高级用法 / Advanced Usage

WavX频谱图分析模块提供了灵活的API，既可以一步完成频谱图生成和显示，也可以分步骤进行以实现更复杂的分析和自定义可视化。
The WavX spectrogram module offers a flexible API that allows for both one-step spectrogram generation and display, as well as step-by-step processing for more complex analysis and custom visualization.

### 步骤 1: 分析频谱图数据 / Step 1: Analyze spectrogram data

```python
import wavx

# 分析频谱图数据 / Analyze spectrogram data
spec_data = wavx.analysis.spectrogram.analyze_spectrogram(
    audio_file="your_audio_file.wav",
    channel=0,           # 0=左声道/left channel, 1=右声道/right channel
    window_size=1024,    # 窗口大小/window size
    overlap=0.75         # 75%的窗口重叠/window overlap
)

# 打印频谱图信息 / Print spectrogram information
wavx.analysis.spectrogram.print_spectrogram_info(spec_data)
```

### 步骤 2: 绘制和显示频谱图 / Step 2: Plot and display spectrogram

```python
import matplotlib.pyplot as plt

# 使用分析好的数据绘制频谱图 / Use the analyzed data to plot the spectrogram
fig = wavx.analysis.spectrogram.plot_spectrogram(
    spec_data=spec_data,
    use_log_scale=True,  # 使用对数刻度显示/use dB scale
    freq_limit=8000,     # 限制频率上限为8kHz/limit to 8kHz
    figsize=(10, 3.5),   # 设置图像大小/figure size
    save_path="spectrogram.png"  # 保存为图像文件/save to file
)

# 可以在这里添加自定义修改 / You can add custom modifications here
plt.axhline(y=1000, color='r', linestyle='--', label='1kHz Reference')
plt.legend()

# 显示图像 / Display the figure
plt.show()
```

## 命令行用法 / Command Line Usage

WavX还提供了命令行工具用于频谱图分析：
WavX also provides a command-line tool for spectrogram analysis:

```bash
# 基本频谱图分析 / Basic spectrogram analysis
wavx spectrogram your_audio_file.wav

# 带参数的频谱图分析 / With parameters
wavx spectrogram your_audio_file.wav --channel 1 --freq-limit 5000 --save output.png

# 使用线性刻度而不是对数刻度 / Use linear scale instead of logarithmic scale
wavx spectrogram your_audio_file.wav --linear
```

## 优化的频谱图显示 / Optimized Spectrogram Display

从v0.1.8版本开始，WavX支持优化的频谱图显示，提供更好的视觉呈现效果：
Starting from v0.1.8, WavX supports optimized spectrogram display for better visual presentation:

```python
# 使用优化的频谱图显示设置
# Use optimized spectrogram display settings
fig = wavx.analysis.spectrogram.plot_spectrogram(
    spec_data=spec_data,
    use_log_scale=True,      # 使用对数刻度/use logarithmic scale
    freq_limit=8000,         # 频率上限/frequency limit
    figsize=(10, 3.5),       # 图形大小/figure size
    colormap='viridis',      # 色彩映射/color map
    dynamic_range=80,        # 动态范围(dB)/dynamic range
    vmin=-100,               # 最小值/minimum value
    vmax=-20                 # 最大值/maximum value
)
```

## API参考 / API Reference

### analyze_spectrogram

```python
analyze_spectrogram(audio_file, channel=0, window_size=1024, overlap=0.75)
```

分析音频文件的频谱图数据。
Analyzes the spectrogram data of an audio file.

**参数 / Parameters:**
- `audio_file` (str): 音频文件路径 / Path to the audio file
- `channel` (int): 要分析的通道 (0=左, 1=右) / Channel to analyze (0=left, 1=right)
- `window_size` (int): 窗口大小 / Window size
- `overlap` (float): 窗口重叠比例 (0.0-1.0) / Window overlap ratio (0.0-1.0)

**返回 / Returns:**
- 包含频谱图数据的字典 / A dictionary containing spectrogram data

### plot_spectrogram

```python
plot_spectrogram(spec_data, use_log_scale=True, freq_limit=None, figsize=(10, 3.5), save_path=None, colormap='viridis', dynamic_range=80, vmin=None, vmax=None)
```

绘制音频的频谱图。
Plots the audio spectrogram.

**参数 / Parameters:**
- `spec_data` (dict): 从analyze_spectrogram获取的频谱图数据 / Spectrogram data from analyze_spectrogram
- `use_log_scale` (bool): 是否使用对数刻度显示 / Whether to use logarithmic scale
- `freq_limit` (int, optional): 频率上限 (Hz)，None表示显示全部 / Frequency limit (Hz), None means show all
- `figsize` (tuple): 图像大小 / Figure size
- `save_path` (str, optional): 如果提供，保存图像到此路径 / If provided, save figure to this path
- `colormap` (str): 色彩映射名称 / Color map name
- `dynamic_range` (float): 动态范围(dB) / Dynamic range in dB
- `vmin` (float, optional): 色彩映射最小值 / Minimum value for color mapping
- `vmax` (float, optional): 色彩映射最大值 / Maximum value for color mapping

**返回 / Returns:**
- matplotlib图形对象 / matplotlib figure object

### display_spectrogram

```python
display_spectrogram(audio_file, channel=0, window_size=1024, overlap=0.75, use_log_scale=True, freq_limit=None, figsize=(10, 3.5), save_path=None, colormap='viridis', dynamic_range=80, vmin=None, vmax=None)
```

分析并显示音频文件的频谱图（一步到位函数）。
Analyzes and displays the spectrogram of an audio file (all-in-one function).

**参数 / Parameters:**
- `audio_file` (str): 音频文件路径 / Path to the audio file
- `channel` (int): 要分析的通道 (0=左, 1=右) / Channel to analyze (0=left, 1=right)
- `window_size` (int): 窗口大小 / Window size
- `overlap` (float): 窗口重叠比例 (0.0-1.0) / Window overlap ratio (0.0-1.0)
- `use_log_scale` (bool): 是否使用对数刻度显示 / Whether to use logarithmic scale
- `freq_limit` (int, optional): 频率上限 (Hz)，None表示显示全部 / Frequency limit (Hz), None means show all
- `figsize` (tuple): 图像大小 / Figure size
- `save_path` (str, optional): 如果提供，保存图像到此路径 / If provided, save figure to this path
- `colormap` (str): 色彩映射名称 / Color map name
- `dynamic_range` (float): 动态范围(dB) / Dynamic range in dB
- `vmin` (float, optional): 色彩映射最小值 / Minimum value for color mapping
- `vmax` (float, optional): 色彩映射最大值 / Maximum value for color mapping

**返回 / Returns:**
- 包含频谱图数据的字典 / A dictionary containing spectrogram data 