# # Define the data as a list of lists
# data = """217 152 127 101 110 330 301 308
# 127 161 136 199 136 138 158 106
# 250 198 75 102 320 58 111 133
# 127 113 147 373 108 368 207 144
# 176 132 150 117 237 125 224 262
# 119 217 283 113 159 175 145 244
# 253 172 124 109 290 242 144 94
# 125 188 225 165 357 131 289 293
# 229 194 137 99 179 147 189 116
# 144 138 273 166 150 216 119 187
# 136 225 74 108 296 144 121 173
# 221 147"""

# # Define the CSV file path
# csv_file = 'data.csv'

# # Write the data to the CSV file
# with open(csv_file, 'w') as file:
#     # Replace spaces AND /n with commas
#     file.write(data.replace(' ', ',').replace('\n', ','))


# print(f'Data has been saved to {csv_file}')

# import pandas as pd
# import matplotlib.pyplot as plt
# import io

# # Define the CSV data as a string
# csv_data = """
# 217,152,127,101,110,330,301,308,127,161,136,199,136,138,158,106,250,198,75,102,320,58,111,133,127,113,147,373,108,368,207,144,176,132,150,117,237,125,224,262,119,217,283,113,159,175,145,244,253,172,124,109,290,242,144,94,125,188,225,165,357,131,289,293,229,194,137,99,179,147,189,116,144,138,273,166,150,216,119,187,136,225,74,108,296,144,121,173,221,147
# """

# # Read the CSV data into a DataFrame
# data = pd.read_csv(io.StringIO(csv_data), header=None)

# # Define the bin width in kilometers
# bin_width_km = 50

# # Calculate the number of bins based on the data range and bin width
# data_min = data.values.min()
# data_max = data.values.max()
# num_bins = int((data_max - data_min) / bin_width_km) + 1

# # Step 3: Create a histogram with 50 km wide bins
# plt.hist(data.values.flatten(), bins=num_bins, range=(data_min, data_max), color='skyblue', edgecolor='black')
# plt.xlabel('Value (km)')
# plt.ylabel('Frequency')
# plt.title('Histogram of CSV Data (50 km Bins)')
# plt.grid(True)

# # Display the histogram
# plt.show()


import io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

csv_data = """
217,152,127,101,110,330,301,308,127,161,136,199,136,138,158,106,250,198,75,102,320,58,111,133,127,113,147,373,108,368,207,144,176,132,150,117,237,125,224,262,119,217,283,113,159,175,145,244,253,172,124,109,290,242,144,94,125,188,225,165,357,131,289,293,229,194,137,99,179,147,189,116,144,138,273,166,150,216,119,187,136,225,74,108,296,144,121,173,221,147
"""

# Read the CSV data into a DataFrame
data = pd.read_csv(io.StringIO(csv_data), header=None)

# Define the bin width in kilometers
bin_width_km = 50

# Calculate the bin edges based on the data range and bin width
data_min = data.values.min()
data_max = data.values.max()
bin_edges = np.arange(50, 400 + bin_width_km, bin_width_km)

# Create the histogram with custom bin edges
hist, bins = np.histogram(data.values, bins=bin_edges)

# Plot the histogram
plt.hist(data.values.flatten(), bins=bin_edges, color='skyblue', edgecolor='black')
plt.xlabel('Number of kilometers driven (km)')
plt.ylabel('Number of students out of 90')
plt.title('Histogram of CSV Data (50 km Bins)')
plt.grid(True)

# Display the histogram
plt.show()