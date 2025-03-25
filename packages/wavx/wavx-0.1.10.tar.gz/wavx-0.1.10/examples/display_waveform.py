#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WavX Waveform Example

Demonstrates how to generate and display waveforms using WavX
"""

import os
import sys
import argparse
import matplotlib.pyplot as plt

# Add project root to Python path to import wavx package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import wavx


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='WavX Waveform Example')
    parser.add_argument('audio_file', help='Path to audio file')
    parser.add_argument('--channel', '-c', type=int, default=0, help='Analysis channel (0=left, 1=right)')
    parser.add_argument('--save', '-s', help='Path to save waveform (e.g., waveform.png)')
    args = parser.parse_args()

    # Basic method: Direct analysis and display
    print("Method 1: Using integrated function to display waveform")
    wavx.analysis.waveform.display_waveform(
        audio_file=args.audio_file,
        channel=args.channel,
        save_path=args.save
    )

    # Advanced method: Step by step processing
    print("\nMethod 2: Step by step waveform processing")
    # 1. Analyze waveform
    waveform_data = wavx.analysis.waveform.analyze_waveform(
        audio_file=args.audio_file,
        channel=args.channel
    )
    
    # 2. Print waveform information
    wavx.analysis.waveform.print_waveform_info(waveform_data)
    
    # 3. Plot waveform
    fig = wavx.analysis.waveform.plot_waveform(
        waveform_data=waveform_data,
        figsize=(10, 6),
        save_path=None  # Don't save, just display
    )
    
    # 4. Add custom plot elements
    plt.axhline(y=0, color='r', linestyle='--', label='Zero Level')
    plt.legend()
    
    # 5. Display modified plot
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main() 