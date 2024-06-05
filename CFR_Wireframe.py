import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# File paths for your data files
filenames = ["f_float1.dat", "f_float2.dat", "f_float3.dat", "f_float4.dat", "f_float5.dat", "f_float6.dat", "f_float7.dat", "NLOS.dat"]

# Starting bin indices for each plot
starting_bin_indices = [1466370, 2383870, 1077240, 40950, 2506750, 49150, 1581060, 847880] # backward , add in value
colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', 'c']
# Sampling rate
sampling_rate = 62.5e6  # 62.5 MS/s
# Center frequency
center_frequency = 3.74e9  # Center frequency in Hz

# Create a figure for 3D wireframe plot
fig = plt.figure(figsize=(10, 25))
ax = fig.add_subplot(111, projection='3d')

# Custom filenames and their corresponding positions along the y-axis
Distances = ["2m", "4m", "6m", "8m", "10m", "12", "NLOS1", "NLOS2"]
y_positions = np.arange(len(Distances))

# Loop through the filenames and process each file
for i, (filename, start_index, color) in enumerate(zip(filenames, starting_bin_indices, colors)):
    # Read data from file
    data = np.fromfile(filename, dtype=np.float32)

    # Take the data starting from the specified start index and ending at index 4100
    num_bins = 4096
    end_index = start_index + num_bins

    # Calculate the frequency axis using the sampling rate
    frequency_resolution = sampling_rate / num_bins
    frequency_axis = np.linspace(center_frequency - sampling_rate / 2, center_frequency + sampling_rate / 2, num_bins)

    # Create a meshgrid for frequency and file index
    X, Y = np.meshgrid(frequency_axis, [i])

    # Plot data as a wireframe with specified color
    ax.plot_wireframe(X, Y, np.array([data[start_index:end_index]]), color=color, label=filename)

# Set labels and title
ax.set_xlabel('Frequency (GHz)')
ax.set_ylabel('Distance')
ax.set_zlabel('Amplitude')
ax.set_title('3D Plot of CFR at different Circumstances')

# Set ytick labels
ax.set_yticks(y_positions)
ax.set_yticklabels(Distances)

# Show the plot
plt.show()

