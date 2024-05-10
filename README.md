# fourier-transform
Signal Processing Toolkit

This Python-based toolkit provides a comprehensive set of tools for signal processing applications. It facilitates the manipulation, analysis, and visualization of signal data, making it an excellent resource for educational purposes or practical signal processing tasks.

Features
File Operations: Read and write signal data, focusing on little-endian two-byte conversions.
Signal Analysis: Parse signals from binary files and adjust for value normalization.
Filtering: Apply first and second-order low-pass and high-pass filters.
Fourier Transform: Analyze frequency components using direct Fourier transforms.
Interactive GUI: Use PySimpleGUI for easy file selection and signal parameter adjustments.
Data Visualization: Plot signals and their transformations with options to toggle data streams on and off.
Installation
To run this script, you'll need Python installed on your machine along with several dependencies.

Prerequisites
Python 3.6 or higher
NumPy
Matplotlib
SciPy
PySimpleGUI
You can install the required packages using pip:

pip install numpy matplotlib scipy PySimpleGUI

Download
Clone the repository to your local machine:

git clone git@github.com:ekacnoom/fourier-transform.git
cd fourier-transform

Usage
To run the script, navigate to the script directory and run:

python signal_processing_toolkit.py

The GUI will guide you through the process of loading a signal file (you can you one of the provided files - 001.bk0 or filename.ts - for testing purposes), adjusting parameters, applying filters, and viewing results.

Examples
Reading and Writing Data:
 - Load a signal data file through the GUI.
 - The script will process and optionally filter the signal as per your settings.
Filtering and Visualization:
 - Apply different filters and observe the effects in real-time on the generated plots.
Fourier Transform Analysis:
 - Perform and visualize a Fourier transform on your signal data to analyze its frequency components.
   
Contributing
Contributions to enhance or expand this toolkit are welcome. Please ensure to follow the standard fork-branch-pull request workflow.

License
This project is licensed under the Apache License 2.0 - see the LICENSE file for details.
