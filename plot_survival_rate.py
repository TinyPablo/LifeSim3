import os
import re
import matplotlib.pyplot as plt
import sys
import time
from matplotlib.animation import FuncAnimation

# Directory containing the files
directory = sys.argv[1]

# Initialize the plot
fig, ax = plt.subplots(figsize=(10, 5))
line, = ax.plot([], [])  # No marker parameter

# Regex pattern to match filenames like "101-96.86.avi"
pattern = re.compile(r'(\d+)-([\d.]+)\.avi')

def update_plot(frame):
    # Initialize lists to store x and y values
    x_values = []
    y_values = []

    # Iterate over files in the directory
    for filename in os.listdir(directory):
        match = pattern.match(filename)
        if match:
            x = int(match.group(1))
            y = float(match.group(2))
            x_values.append(x)
            y_values.append(y)

    # Sort the values by x
    sorted_indices = sorted(range(len(x_values)), key=lambda i: x_values[i])
    x_values = [x_values[i] for i in sorted_indices]
    y_values = [y_values[i] for i in sorted_indices]

    # Update the data in the plot
    line.set_data(x_values, y_values)
    ax.relim()
    ax.autoscale_view()

    return line,

# Animation function with 1-second interval
ani = FuncAnimation(fig, update_plot, interval=1000)

# Plot settings
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('Plot of x vs y from filenames')
ax.grid(True)

# Show the plot
plt.show()
