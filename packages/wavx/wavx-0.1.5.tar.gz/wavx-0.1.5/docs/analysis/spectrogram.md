# 音频频谱图分析

WavX提供了功能强大的频谱图分析工具，能够可视化音频文件的时频特性。

## 基本用法

```python
import wavx

# 分析并显示频谱图
wavx.analysis.spectrogram.display_spectrogram("your_audio_file.wav")
```

## 高级用法

WavX频谱图分析模块提供了灵活的API，既可以一步完成频谱图生成和显示，也可以分步骤进行以实现更复杂的分析和自定义可视化。

### 步骤 1: 分析频谱图数据

```python
import wavx

# 分析频谱图数据
spec_data = wavx.analysis.spectrogram.analyze_spectrogram(
    audio_file="your_audio_file.wav",
    channel=0,  # 0=左声道, 1=右声道
    window_size=None,  # 自动设置窗口大小
    overlap=0.75  # 75%的窗口重叠
)

# 打印频谱图信息
wavx.analysis.spectrogram.print_spectrogram_info(spec_data)
```

### 步骤 2: 绘制和显示频谱图

```python
import matplotlib.pyplot as plt

# 使用分析好的数据绘制频谱图
fig = wavx.analysis.spectrogram.plot_spectrogram(
    spec_data=spec_data,
    use_log_scale=True,  # 使用对数刻度显示
    freq_limit=8000,     # 限制频率上限为8kHz
    figsize=(12, 4),     # 设置图像大小
    save_path="spectrogram.png"  # 保存为图像文件
)

# 可以在这里添加自定义修改
plt.axhline(y=1000, color='r', linestyle='--', label='1kHz参考线')
plt.legend()

# 显示图像
plt.show()
```

## 命令行用法

WavX还提供了命令行工具用于频谱图分析：

```bash
# 基本频谱图分析
wavx spectrogram your_audio_file.wav

# 带参数的频谱图分析
wavx spectrogram your_audio_file.wav --channel 1 --freq-limit 5000 --save output.png

# 使用线性刻度而不是对数刻度
wavx spectrogram your_audio_file.wav --linear
```

## API参考

### analyze_spectrogram

```python
analyze_spectrogram(audio_file, channel=0, window_size=None, overlap=0.75)
```

分析音频文件的频谱图数据。

**参数:**
- `audio_file` (str): 音频文件路径
- `channel` (int): 要分析的通道 (0=左, 1=右)
- `window_size` (int, optional): 窗口大小，None表示自动设置
- `overlap` (float): 窗口重叠比例 (0.0-1.0)

**返回:**
- 包含频谱图数据的字典

### plot_spectrogram

```python
plot_spectrogram(spec_data, use_log_scale=True, freq_limit=None, figsize=(12, 4), save_path=None)
```

绘制音频的频谱图。

**参数:**
- `spec_data` (dict): 从analyze_spectrogram获取的频谱图数据
- `use_log_scale` (bool): 是否使用对数刻度显示
- `freq_limit` (int, optional): 频率上限 (Hz)，None表示显示全部
- `figsize` (tuple): 图像大小
- `save_path` (str, optional): 如果提供，保存图像到此路径

**返回:**
- matplotlib图形对象

### display_spectrogram

```python
display_spectrogram(audio_file, channel=0, window_size=None, overlap=0.75, use_log_scale=True, freq_limit=None, figsize=(12, 4), save_path=None)
```

分析并显示音频文件的频谱图（一步到位函数）。

**参数:**
- `audio_file` (str): 音频文件路径
- `channel` (int): 要分析的通道 (0=左, 1=右)
- `window_size` (int, optional): 窗口大小，None表示自动设置
- `overlap` (float): 窗口重叠比例 (0.0-1.0)
- `use_log_scale` (bool): 是否使用对数刻度显示
- `freq_limit` (int, optional): 频率上限 (Hz)，None表示显示全部
- `figsize` (tuple): 图像大小
- `save_path` (str, optional): 如果提供，保存图像到此路径

**返回:**
- 包含频谱图数据的字典 