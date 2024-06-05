import numpy as np
import matplotlib.pyplot as plt

float_dtype = np.float32
dtype = np.complex64

# Read PSD data
filename_pdp = "f_float3.dat"
data_pdp = np.fromfile(open(filename_pdp, 'rb'), dtype=float_dtype)

# Sampling Rate
SR = 62.500000e6 * 1e-6
PSD_Rang = 1000000  # Range of data to be plotted for CFR

# Center frequency
center_freq = 3.74e9  # 3.74 GHz

# Bin starting index (modify as needed)
start_bin_index = 0

# Convert bin index to frequency for PSD
frequency_axis_pdp = np.fft.fftfreq(len(data_pdp[:PSD_Rang]), d=1/SR) + center_freq

# Create a separate figure for PSD data (magnitude vs bins)
fig_psd_bins, ax_psd_bins = plt.subplots(figsize=(10, 6))
ax_psd_bins.plot(np.arange(start_bin_index, len(data_pdp[:PSD_Rang]) + start_bin_index), (data_pdp[:PSD_Rang]))
ax_psd_bins.set_xlabel('Bins')
ax_psd_bins.set_ylabel('Magnitude')
ax_psd_bins.set_title('PSD Magnitude vs Bins')

# Create a separate figure for PSD data (magnitude vs frequency)
fig_psd_freq, ax_psd_freq = plt.subplots(figsize=(10, 6))
ax_psd_freq.plot(frequency_axis_pdp, (data_pdp[:PSD_Rang]))
ax_psd_freq.set_xlabel('Frequency (Hz)')
ax_psd_freq.set_ylabel('Magnitude')
ax_psd_freq.set_title('PSD Magnitude vs Frequency')

plt.show()
