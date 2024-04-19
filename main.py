import colour.plotting
import matplotlib.pyplot as plt
import pandas as pd
import re

def hex_to_rgb(hex):
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

# basic diagram
fig, ax = colour.plotting.plot_chromaticity_diagram_CIE1931()
fig.patch.set_alpha(1)

# get user input
searchterm = input("Enter color to visualize: ")

if searchterm == "":
    fig.savefig('plots/CIE1931_Chromaticity_Diagram.png')
    exit()

# load data
print("Loading and filtering data")
data = pd.read_csv('data/colornames.csv')

# filter data
threshold = 6
data = data[data['votes'] >= threshold]

# search for color
pattern = r"\b" + re.escape(searchterm) + r"\b"
colors = data[data['bestName'].str.contains(pattern, case=False, regex=True)]

if len(colors) == 0:
    print("No colors found")
    exit()

print("Some examples of colors that match your search term:")
print(colors.head())

# plot colors
print(f"Plotting {len(colors)} colors")
x, y = list(zip(*[colour.convert(hex_to_rgb(colors.iloc[i]['hexCode']),"RGB","CIE xy") for i in range(len(colors))]))

print("Scattering")
ax.scatter(x, y, color='black', s=3, alpha=0.1)

# save plot
print(f"Saving plot to 'plots/CIE1931_Chromaticity_Diagram_{searchterm}.png'")
fig.savefig(f'plots/CIE1931_Chromaticity_Diagram_{searchterm}.png', dpi=300)

print("Done!")