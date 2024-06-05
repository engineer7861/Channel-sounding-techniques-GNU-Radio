import numpy as np
import matplotlib.pyplot as plt

# File paths for your data files
filenames = ["f_float1.dat", "f_float2.dat", "f_float3.dat", "f_float4.dat", "f_float5.dat", "f_float6.dat", "f_float7.dat", "NLOS.dat"]

# Descriptive labels for each plot
labels = ["2m", "4m", "6m", "8m", "10m", "12m", "NLOS1", "NLOS2"]

# Starting bin indices for each plot
starting_bin_indices = [1466370, 2383870, 1077240, 40950, 2506750, 49150, 1581060, 847880] # backward , add in value

# Create a figure with subplots
fig, axs = plt.subplots(8, 1, figsize=(10, 20), sharex=True)

# Loop through the filenames and process each file
for i, (filename, label, start_index) in enumerate(zip(filenames, labels, starting_bin_indices)):
    # Read data from file
    data = np.fromfile(filename, dtype=np.float32)

    # Take the data starting from the specified start index and ending at index 55000
    data = data[start_index:start_index + 4096]  # 6190 or 4100 bins are required

    # Plot data on the corresponding subplot and set the label as the descriptive label
    axs[i].plot(data, label=label)
    axs[i].set_ylabel('Amplitude')

    # Add legend to each subplot
    axs[i].legend()

# Set common x-label
axs[-1].set_xlabel('Bin Index')

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()
