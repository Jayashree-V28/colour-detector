import pandas as pd
import math

# Load color dataset
def load_colors(csv_path):
    return pd.read_csv(csv_path)

# Get closest color name
def get_closest_color_name(r, g, b, color_data):
    min_dist = float('inf')
    closest_color = None

    for _, row in color_data.iterrows():
        d = math.sqrt((r - row['R'])**2 + (g - row['G'])**2 + (b - row['B'])**2)
        if d < min_dist:
            min_dist = d
            closest_color = row

    return closest_color['color_name'], (closest_color['R'], closest_color['G'], closest_color['B']), closest_color['hex']
