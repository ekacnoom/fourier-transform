import filters as f
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from matplotlib.widgets import CheckButtons
import PySimpleGUI as sg

# This function takes a sequence of numbers and writes them to a file in the little-endian format of two-byte numbers
def write_bytes_to_file(seq, filename):
    with open(filename, "wb") as file:
        for i in seq:
            n = i if i >= 0 else 65535 + i
            res = int(n).to_bytes(2, 'little')
            file.write(res)

# This function reads the signal from the input file, which is split into two-byte blocks, then converted into integers. If the number exceeds 5000, it is subtracted from 65535 to normalise the values. The resultant signal values are returned as a list y
def parse_signal(input_file):
    chunk_size = 2
    y = []
    while True:
        chunk = input_file.read(chunk_size)
        if not chunk:
            break
        y_i = int.from_bytes(chunk, 'little')
        if y_i > 5000:
            y_i -= 65535
        y.append(y_i)

    return y

# This function copies bytes from the input file to a new file named filename.dat. During the copying process, negative numbers are converted to their positive equivalents
def copy_bytes_to_file(input_filename):
    output_filename = 'filename.dat'
    with open(input_filename, 'rb') as input_file, open(output_filename, 'wb') as output_file:
        while True:
            chunk = input_file.read(2)  # Reading a byte block (using a block size of 2 here)
            if not chunk:  # If there are no more data, we end the loop
                break
            n = int.from_bytes(chunk, byteorder='little', signed=True)  # Converting bytes to an integer
            if n < 0:  # If the number is negative, we convert it to a positive
                n = 65535 + n
            b = n.to_bytes(2, byteorder='little')  # Converting the integer back to bytes
            output_file.write(b)  # Writing the bytes to the output file

# This function opens a file selection window using the PySimpleGUI library and returns the file path selected by the user
def choose_file():
    sg.theme('SystemDefault')  # Choosing a theme
    layout = [[sg.Text('Select a file:')],
              [sg.Input(), sg.FileBrowse(key='-FILE-')],
              [sg.Button('Ok')]]
    window = sg.Window('File Selection', layout)
    event, values = window.read()
    window.close()
    return values['-FILE-']

# Window for adjusting signal parameters
layout = [[sg.Text('Signal parameters')],
          [sg.Text('Sampling rate (measurements per second)')],
          [sg.InputText('1000', key='-FS-')],
          [sg.Text('Duration of signal in seconds')],
          [sg.InputText('1', key='-T-')],
          [sg.Text('Frequencies (comma-separated)')],
          [sg.InputText('50, 60, 400', key='-FREQUENCIES-')],
          [sg.Text('Amplitudes (comma-separated)')],
          [sg.InputText('220, 110, 36', key='-AMPLITUDES-')],
          [sg.Button('Apply')]]
window = sg.Window('Adjust Signal Parameters', layout)
event, values = window.read()
window.close()

# Updating signal parameters
fs = int(values['-FS-'])
T = float(values['-T-'])
frequencies = [int(x) for x in values['-FREQUENCIES-'].split(',')]
amplitudes = [int(x) for x in values['-AMPLITUDES-'].split(',')]

# Generating a new signal
N = int(fs * T)
dt = 1 / fs
t = np.arange(N) * dt
x = np.sum([amplitudes[i] * np.sin(2 * np.pi * frequencies[i] * t)
            for i in range(len(frequencies))], axis=0)
# Saving the test signal to a file
filename = 'filename.tst'
write_bytes_to_file(x, filename)
copy_bytes_to_file(filename)

signal = parse_signal(open(choose_file(), 'rb'))

# Applying a simple first-order low-pass filter
filtered_data_1 = f.apply_lowpass_filter(signal, order=1)
filtered_filename_1 = 'filename.da1'
write_bytes_to_file(filtered_data_1, filtered_filename_1)

# Applying a simple first-order high-pass filter
filtered_data_2 = f.apply_highpass_filter(signal, order=1)
filtered_filename_2 = 'filename.da2'
write_bytes_to_file(filtered_data_2, filtered_filename_2)

# Applying a simple second-order low-pass filter
filtered_data_3 = f.apply_lowpass_filter(signal, order=2)
filtered_filename_3 = 'filename.da3'
write_bytes_to_file(filtered_data_3, filtered_filename_3)

# Applying a simple second-order high-pass filter
filtered_data_4 = f.apply_highpass_filter(signal, order=2)
filtered_filename_4 = 'filename.da4'
write_bytes_to_file(filtered_data_4, filtered_filename_4)

# Direct Fourier Transform
freqs = fftfreq(N, dt)[:N//2]
fftres = fft(signal)

# Creating a window for signal and filter graphs
fig, ax = plt.subplots(figsize=(16, 9))
plt.title('Signal and Filter Graphs')

# Display settings for the signal and filter graphs
plt.subplots_adjust(top=0.9, bottom=0.2, left=0.1, right=0.9)
l1, = ax.plot(t, signal, label='Initial Signal', color='blue')
l2, = ax.plot(t, filtered_data_1, label='First-Order Low-Pass Filter', color='red')
l3, = ax.plot(t, filtered_data_2, label='First-Order High-Pass Filter', color='green')
l4, = ax.plot(t, filtered_data_3, label='Second-Order Low-Pass Filter', color='purple')
l5, = ax.plot(t, filtered_data_4, label='Second-Order High-Pass Filter', color='orange')

# Axis labels for the signal and filter graphs
ax.set_xlabel('Time, s')
ax.set_ylabel('Amplitude')

# Legend for the signal and filter graphs
lines = [l1, l2, l3, l4, l5]
labels = [line.get_label() for line in lines]
ax.legend(lines, labels, loc='upper right')

# Creating selection buttons
rax = plt.axes([0.1, 0.05, 0.28, 0.1])
check = CheckButtons(rax, labels, [True] * len(labels))

# Function to execute on selection button state change
def update_visibility(label):
    for line, state in zip(lines, check.get_status()):
        line.set_visible(state)
    plt.draw()

check.on_clicked(update_visibility)

# Creating a window for the Direct Fourier Transform graph
fig_fft, ax_fft = plt.subplots(figsize=(10, 8))

# Display settings for the Direct Fourier Transform graph
ax_fft.plot(freqs, 2.0/N * np.abs(fftres[0:N//2]))
ax_fft.set_title('Direct Fourier Transform')
ax_fft.set_xlabel('Frequency (Hz)')
ax_fft.set_ylabel('Amplitude')
ax_fft.grid(True)

plt.show()
