#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Waveform Analysis Module

Provides functionality for audio waveform visualization
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import soundfile as sf
from typing import Dict, Any, Tuple, Optional

def set_plot_style():
    """
    Set plot style using Times New Roman font
    """
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.rcParams['mathtext.fontset'] = 'stix'  # Math formula font
    plt.rcParams['axes.unicode_minus'] = False  # Correct minus sign display

def analyze_waveform(audio_file: str, channel: int = 0) -> Dict[str, Any]:
    """
    Analyze audio file waveform

    Args:
        audio_file: Path to audio file
        channel: Channel to analyze (0=left, 1=right)

    Returns:
        Dictionary containing waveform data
    """
    # Read audio file
    try:
        sample_rate, data = wavfile.read(audio_file)
        # Check file type, use soundfile if not WAV
        if data.dtype == 'float32' or data.dtype == 'float64':
            data = np.iinfo(np.int16).max * data
    except:
        # Try soundfile if wavfile fails
        data, sample_rate = sf.read(audio_file)
        # Normalize to 16-bit integer range
        if data.dtype == 'float32' or data.dtype == 'float64':
            data = np.iinfo(np.int16).max * data

    # If stereo, take specified channel
    if data.ndim > 1:
        if channel >= data.shape[1]:
            channel = 0  # Use first channel if specified is unavailable
        data = data[:, channel]

    # Generate time axis
    time = np.arange(len(data)) / sample_rate

    return {
        'audio_file': audio_file,
        'sample_rate': sample_rate,
        'data': data,
        'time': time,
        'channel': channel
    }

def plot_waveform(waveform_data: Dict[str, Any],
                  figsize: Tuple[int, int] = (12, 4),
                  save_path: Optional[str] = None) -> plt.Figure:
    """
    Plot audio waveform

    Args:
        waveform_data: Waveform data from analyze_waveform
        figsize: Figure size
        save_path: If provided, save figure to this path

    Returns:
        matplotlib figure object
    """
    # Set plot style
    set_plot_style()

    # Create figure
    fig = plt.figure(figsize=figsize)

    # Plot waveform
    plt.plot(waveform_data['time'], waveform_data['data'])

    # Set title and labels
    audio_file = waveform_data['audio_file'].split("/")[-1]
    plt.title(f"Waveform: {audio_file}", pad=10)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)

    # Optimize layout
    plt.tight_layout()

    # Save figure
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')

    return fig

def print_waveform_info(waveform_data: Dict[str, Any]) -> None:
    """
    Print waveform analysis information

    Args:
        waveform_data: Waveform data from analyze_waveform
    """
    print(f"Audio file: {waveform_data['audio_file']}")
    print(f"Sample rate: {waveform_data['sample_rate']} Hz")
    print(f"Data length: {len(waveform_data['data'])} samples")
    print(f"Duration: {len(waveform_data['data']) / waveform_data['sample_rate']:.2f} seconds")
    print(f"Channel: {waveform_data['channel']}")

def display_waveform(audio_file: str,
                    channel: int = 0,
                    figsize: Tuple[int, int] = (12, 4),
                    save_path: Optional[str] = None) -> None:
    """
    Analyze and display audio file waveform

    Args:
        audio_file: Path to audio file
        channel: Channel to analyze (0=left, 1=right)
        figsize: Figure size
        save_path: If provided, save figure to this path
    """
    # Analyze waveform
    waveform_data = analyze_waveform(
        audio_file=audio_file,
        channel=channel
    )

    # Print information
    print_waveform_info(waveform_data)

    # Plot and display waveform
    fig = plot_waveform(
        waveform_data=waveform_data,
        figsize=figsize,
        save_path=save_path
    )

    plt.show()

    return waveform_data 