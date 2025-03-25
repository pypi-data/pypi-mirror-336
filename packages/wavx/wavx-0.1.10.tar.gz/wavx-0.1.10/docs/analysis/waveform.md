# Audio Waveform Visualization

WavX provides powerful tools for audio waveform visualization that help you analyze and understand the time-domain characteristics of audio signals.

## Basic Usage

```python
import wavx

# Analyze and display waveform
wavx.analysis.waveform.display_waveform("your_audio_file.wav")
```

## Advanced Usage

The WavX waveform module offers a flexible API that allows for both one-step waveform generation and display, as well as step-by-step processing for more complex analysis and custom visualization.

### Step 1: Analyze waveform data

```python
import wavx

# Analyze waveform data
waveform_data = wavx.analysis.waveform.analyze_waveform(
    audio_file="your_audio_file.wav",
    channel=0  # 0=left channel, 1=right channel
)

# Print waveform information
wavx.analysis.waveform.print_waveform_info(waveform_data)
```

### Step 2: Plot and display waveform

```python
import matplotlib.pyplot as plt

# Use the analyzed data to plot the waveform
fig = wavx.analysis.waveform.plot_waveform(
    waveform_data=waveform_data,
    figsize=(12, 4),     # figure size
    save_path="waveform.png",  # save to file
    color="Olive Green"  # use predefined color scheme
)

# You can add custom modifications here
plt.axhline(y=0, color='r', linestyle='--', label='Zero Level')
plt.legend()

# Display the figure
plt.show()
```

## Color Schemes

WavX v0.1.8 introduced predefined color schemes for waveform visualization:

```python
# Available color schemes:
wavx.analysis.waveform.plot_waveform(
    waveform_data=waveform_data,
    color="Aqua Gray"    # use this color scheme
)

# Available colors:
# - "Aqua Gray": "#7FBFBF"
# - "Muted Purple": "#9E91B7"
# - "Olive Green": "#9DB17C" (default)
# - "Soft Coral": "#E1A193"
# - "Slate Blue": "#7A8B99"
# - "Dusty Rose": "#C2A9A1"
```

You can also use direct hex color codes:

```python
wavx.analysis.waveform.plot_waveform(
    waveform_data=waveform_data,
    color="#FF5733"  # custom hex color
)
```

## Command Line Usage

WavX also provides a command-line tool for waveform visualization:

```bash
# Basic waveform visualization
wavx waveform your_audio_file.wav

# With parameters
wavx waveform your_audio_file.wav --channel 1 --save output.png

# With color scheme
wavx waveform your_audio_file.wav --color "Soft Coral"
```

## API Reference

### analyze_waveform

```python
analyze_waveform(audio_file, channel=0)
```

Analyzes the waveform of an audio file.

**Parameters:**
- `audio_file` (str): Path to the audio file
- `channel` (int): Channel to analyze (0=left, 1=right)

**Returns:**
- A dictionary containing waveform data

### plot_waveform

```python
plot_waveform(waveform_data, figsize=(12, 4), save_path=None, color="Olive Green")
```

Plots the audio waveform.

**Parameters:**
- `waveform_data` (dict): Waveform data from analyze_waveform
- `figsize` (tuple): Figure size
- `save_path` (str, optional): If provided, save figure to this path
- `color` (str): Color scheme name or hex color code

**Returns:**
- matplotlib figure object

### display_waveform

```python
display_waveform(audio_file, channel=0, figsize=(12, 4), save_path=None, color="Olive Green")
```

Analyzes and displays the waveform of an audio file (all-in-one function).

**Parameters:**
- `audio_file` (str): Path to the audio file
- `channel` (int): Channel to analyze (0=left, 1=right)
- `figsize` (tuple): Figure size
- `save_path` (str, optional): If provided, save figure to this path
- `color` (str): Color scheme name or hex color code

**Returns:**
- A dictionary containing waveform data 