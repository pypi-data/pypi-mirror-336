#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
WavX Spectrogram Example

Demonstrates how to generate and display spectrograms using WavX
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
    parser = argparse.ArgumentParser(description='WavX Spectrogram Example')
    parser.add_argument('audio_file', help='Path to audio file')
    parser.add_argument('--channel', '-c', type=int, default=0, help='Analysis channel (0=left, 1=right)')
    parser.add_argument('--freq-limit', '-f', type=int, default=8000, help='Frequency limit (Hz)')
    parser.add_argument('--linear', action='store_true', help='Use linear scale instead of log scale')
    parser.add_argument('--save', '-s', help='Path to save spectrogram (e.g., spectrogram.png)')
    args = parser.parse_args()

    # Basic method: Direct analysis and display
    print("Method 1: Using integrated function to display spectrogram")
    wavx.analysis.spectrogram.display_spectrogram(
        audio_file=args.audio_file,
        channel=args.channel,
        use_log_scale=not args.linear,
        freq_limit=args.freq_limit,
        save_path=args.save
    )

    # Advanced method: Step by step processing
    print("\nMethod 2: Step by step spectrogram processing")
    # 1. Analyze spectrogram
    spec_data = wavx.analysis.spectrogram.analyze_spectrogram(
        audio_file=args.audio_file,
        channel=args.channel
    )
    
    # 2. Print spectrogram information
    wavx.analysis.spectrogram.print_spectrogram_info(spec_data)
    
    # 3. Plot spectrogram
    fig = wavx.analysis.spectrogram.plot_spectrogram(
        spec_data=spec_data,
        use_log_scale=not args.linear,
        freq_limit=args.freq_limit,
        figsize=(10, 6),
        save_path=None  # Don't save, just display
    )
    
    # 4. Add custom plot elements
    plt.axhline(y=1000, color='r', linestyle='--', label='1kHz Reference')
    plt.legend()
    
    # 5. Display modified plot
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main() 