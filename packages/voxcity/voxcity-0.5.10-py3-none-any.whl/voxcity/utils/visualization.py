import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from tqdm import tqdm
import matplotlib.colors as mcolors
from matplotlib.colors import ListedColormap, BoundaryNorm
import matplotlib.cm as cm
import contextily as ctx
from shapely.geometry import Polygon
import plotly.graph_objects as go
from tqdm import tqdm
import pyproj
# import rasterio
from pyproj import CRS
# from shapely.geometry import box
import seaborn as sns
import random
import folium
import math
import trimesh
import pyvista as pv
from IPython.display import display
import os

from .lc import get_land_cover_classes
# from ..geo.geojson import filter_buildings
from ..geoprocessor.grid import (
    calculate_grid_size,
    create_coordinate_mesh,
    create_cell_polygon,
    grid_to_geodataframe
)
from ..geoprocessor.utils import (
    initialize_geod,
    calculate_distance,
    normalize_to_one_meter,
    setup_transformer,
    transform_coords,
)
from ..geoprocessor.mesh import (
    create_voxel_mesh,
    create_sim_surface_mesh,
    create_city_meshes,
    export_meshes,
    save_obj_from_colored_mesh
)
# from ..exporter.obj import save_obj_from_colored_mesh
from .material import get_material_dict

# def get_voxel_color_map():
#     return {
#         -99: [0, 0, 0],  # void,
#         -30: [255, 0, 102],  # (Pink) 'Landmark',
#         -17: [238, 242, 234],  # (light gray) 'plaster',
#         -16: [56, 78, 84],  # (Dark blue) 'glass',
#         -15: [147, 140, 114],  # (Light brown) 'stone',
#         -14: [139, 149, 159],  # (Gray) 'metal',
#         -13: [186, 187, 181],  # (Gray) 'concrete',
#         -12: [248, 166, 2],  # (Orange) 'wood',
#         -11: [81, 59, 56],  # (Dark red) 'brick',
#         -3: [180, 187, 216],  # Building
#         -2: [78, 99, 63],     # Tree
#         -1: [188, 143, 143],  # Underground
#         1: [239, 228, 176],   # 'Bareland (ground surface)',
#         2: [123, 130, 59],   # 'Rangeland (ground surface)',
#         3: [97, 140, 86],   # 'Shrub (ground surface)',
#         4: [112, 120, 56],   #  'Agriculture land (ground surface)',
#         5: [116, 150, 66],   #  'Tree (ground surface)',
#         6: [187, 204, 40],   #  'Moss and lichen (ground surface)',
#         7: [77, 118, 99],    #  'Wet land (ground surface)',
#         8: [22, 61, 51],    #  'Mangrove (ground surface)',
#         9: [44, 66, 133],    #  'Water (ground surface)',
#         10: [205, 215, 224],    #  'Snow and ice (ground surface)',
#         11: [108, 119, 129],   #  'Developed space (ground surface)',
#         12: [59, 62, 87],      # 'Road (ground surface)',
#         13: [150, 166, 190],    #  'Building (ground surface)'
#         14: [239, 228, 176],    #  'No Data (ground surface)'
#     }

def get_voxel_color_map(color_scheme='default'):
    """
    Returns a color map for voxel visualization based on the specified color scheme.
    
    Parameters:
    -----------
    color_scheme : str, optional
        The name of the color scheme to use. Options are:
        - 'default': The original color scheme
        - 'high_contrast': High contrast colors for better visibility
        - 'monochrome': Shades of blue
        - 'pastel': Softer, more muted colors
        - 'dark_mode': Darker colors overall
        - 'grayscale': Black and white gradient
        - 'autumn': Warm reds, oranges, and browns
        - 'cool': Cool blues, purples, and cyans
        - 'earth_tones': Natural earth colors
        - 'vibrant': Very bright, saturated colors
        
        # NEW:
        - 'cyberpunk': Neon-like purples, pinks, and blues
        - 'tropical': Vibrant greens, oranges, pinks (island vibes)
        - 'vintage': Muted, sepia-like tones
        - 'neon_dreams': Super-bright, nightclub neon palette

    Returns:
    --------
    dict
        A dictionary mapping voxel IDs to RGB color values
    """
    # ----------------------
    # DO NOT MODIFY DEFAULT
    # ----------------------
    if color_scheme == 'default':
        return {
            -99: [0, 0, 0],  # void,
            -30: [255, 0, 102],  # (Pink) 'Landmark',
            -17: [238, 242, 234],  # (light gray) 'plaster',
            -16: [56, 78, 84],  # (Dark blue) 'glass',
            -15: [147, 140, 114],  # (Light brown) 'stone',
            -14: [139, 149, 159],  # (Gray) 'metal',
            -13: [186, 187, 181],  # (Gray) 'concrete',
            -12: [248, 166, 2],  # (Orange) 'wood',
            -11: [81, 59, 56],  # (Dark red) 'brick',
            -3: [180, 187, 216],  # Building
            -2: [78, 99, 63],     # Tree
            -1: [188, 143, 143],  # Underground
            1: [239, 228, 176],   # 'Bareland (ground surface)',
            2: [123, 130, 59],    # 'Rangeland (ground surface)',
            3: [97, 140, 86],     # 'Shrub (ground surface)',
            4: [112, 120, 56],    # 'Agriculture land (ground surface)',
            5: [116, 150, 66],    # 'Tree (ground surface)',
            6: [187, 204, 40],    # 'Moss and lichen (ground surface)',
            7: [77, 118, 99],     # 'Wet land (ground surface)',
            8: [22, 61, 51],      # 'Mangrove (ground surface)',
            9: [44, 66, 133],     # 'Water (ground surface)',
            10: [205, 215, 224],  # 'Snow and ice (ground surface)',
            11: [108, 119, 129],  # 'Developed space (ground surface)',
            12: [59, 62, 87],     # 'Road (ground surface)',
            13: [150, 166, 190],  # 'Building (ground surface)'
            14: [239, 228, 176],  # 'No Data (ground surface)'
        }

    elif color_scheme == 'high_contrast':
        return {
            -99: [0, 0, 0],  # void
            -30: [255, 0, 255],  # (Bright Magenta) 'Landmark'
            -17: [255, 255, 255],  # (Pure White) 'plaster'
            -16: [0, 0, 255],  # (Bright Blue) 'glass'
            -15: [153, 76, 0],  # (Dark Brown) 'stone'
            -14: [192, 192, 192],  # (Silver) 'metal'
            -13: [128, 128, 128],  # (Gray) 'concrete'
            -12: [255, 128, 0],  # (Bright Orange) 'wood'
            -11: [153, 0, 0],  # (Dark Red) 'brick'
            -3: [0, 255, 255],  # (Cyan) Building
            -2: [0, 153, 0],  # (Green) Tree
            -1: [204, 0, 102],  # (Dark Pink) Underground
            1: [255, 255, 153],  # (Light Yellow) 'Bareland'
            2: [102, 153, 0],  # (Olive Green) 'Rangeland'
            3: [0, 204, 0],  # (Bright Green) 'Shrub'
            4: [153, 204, 0],  # (Yellowish Green) 'Agriculture land'
            5: [0, 102, 0],  # (Dark Green) 'Tree'
            6: [204, 255, 51],  # (Lime Green) 'Moss and lichen'
            7: [0, 153, 153],  # (Teal) 'Wet land'
            8: [0, 51, 0],  # (Very Dark Green) 'Mangrove'
            9: [0, 102, 204],  # (Bright Blue) 'Water'
            10: [255, 255, 255],  # (White) 'Snow and ice'
            11: [76, 76, 76],  # (Dark Gray) 'Developed space'
            12: [0, 0, 0],  # (Black) 'Road'
            13: [102, 102, 255],  # (Light Purple) 'Building'
            14: [255, 204, 153],  # (Light Orange) 'No Data'
        }

    elif color_scheme == 'monochrome':
        return {
            -99: [0, 0, 0],  # void
            -30: [28, 28, 99],  # 'Landmark'
            -17: [242, 242, 242],  # 'plaster'
            -16: [51, 51, 153],  # 'glass'
            -15: [102, 102, 204],  # 'stone'
            -14: [153, 153, 204],  # 'metal'
            -13: [204, 204, 230],  # 'concrete'
            -12: [76, 76, 178],  # 'wood'
            -11: [25, 25, 127],  # 'brick'
            -3: [179, 179, 230],  # Building
            -2: [51, 51, 153],  # Tree
            -1: [102, 102, 178],  # Underground
            1: [230, 230, 255],  # 'Bareland'
            2: [128, 128, 204],  # 'Rangeland'
            3: [102, 102, 204],  # 'Shrub'
            4: [153, 153, 230],  # 'Agriculture land'
            5: [76, 76, 178],  # 'Tree'
            6: [204, 204, 255],  # 'Moss and lichen'
            7: [76, 76, 178],  # 'Wet land'
            8: [25, 25, 127],  # 'Mangrove'
            9: [51, 51, 204],  # 'Water'
            10: [242, 242, 255],  # 'Snow and ice'
            11: [128, 128, 178],  # 'Developed space'
            12: [51, 51, 127],  # 'Road'
            13: [153, 153, 204],  # 'Building'
            14: [230, 230, 255],  # 'No Data'
        }

    elif color_scheme == 'pastel':
        return {
            -99: [0, 0, 0],  # void
            -30: [255, 179, 217],  # (Pastel Pink) 'Landmark'
            -17: [245, 245, 245],  # (Off White) 'plaster'
            -16: [173, 196, 230],  # (Pastel Blue) 'glass'
            -15: [222, 213, 196],  # (Pastel Brown) 'stone'
            -14: [211, 219, 226],  # (Pastel Gray) 'metal'
            -13: [226, 226, 226],  # (Light Gray) 'concrete'
            -12: [255, 223, 179],  # (Pastel Orange) 'wood'
            -11: [204, 168, 166],  # (Pastel Red) 'brick'
            -3: [214, 217, 235],   # (Pastel Purple) Building
            -2: [190, 207, 180],   # (Pastel Green) Tree
            -1: [235, 204, 204],   # (Pastel Pink) Underground
            1: [250, 244, 227],    # (Cream) 'Bareland'
            2: [213, 217, 182],    # (Pastel Olive) 'Rangeland'
            3: [200, 226, 195],    # (Pastel Green) 'Shrub'
            4: [209, 214, 188],    # (Pastel Yellow-Green) 'Agriculture land'
            5: [195, 220, 168],    # (Light Pastel Green) 'Tree'
            6: [237, 241, 196],    # (Pastel Yellow) 'Moss and lichen'
            7: [180, 210, 205],    # (Pastel Teal) 'Wet land'
            8: [176, 196, 190],    # (Darker Pastel Teal) 'Mangrove'
            9: [188, 206, 235],    # (Pastel Blue) 'Water'
            10: [242, 245, 250],   # (Light Blue-White) 'Snow and ice'
            11: [209, 213, 219],   # (Pastel Gray) 'Developed space'
            12: [189, 190, 204],   # (Pastel Blue-Gray) 'Road'
            13: [215, 221, 232],   # (Very Light Pastel Blue) 'Building'
            14: [250, 244, 227],   # (Cream) 'No Data'
        }

    elif color_scheme == 'dark_mode':
        return {
            -99: [0, 0, 0],  # void
            -30: [153, 51, 102],   # (Dark Pink) 'Landmark'
            -17: [76, 76, 76],     # (Dark Gray) 'plaster'
            -16: [33, 46, 51],     # (Very Dark Blue) 'glass'
            -15: [89, 84, 66],     # (Very Dark Brown) 'stone'
            -14: [83, 89, 94],     # (Dark Gray) 'metal'
            -13: [61, 61, 61],     # (Dark Gray) 'concrete'
            -12: [153, 102, 0],    # (Dark Orange) 'wood'
            -11: [51, 35, 33],     # (Very Dark Red) 'brick'
            -3: [78, 82, 99],      # (Dark Purple) Building
            -2: [46, 58, 37],      # (Dark Green) Tree
            -1: [99, 68, 68],      # (Dark Pink) Underground
            1: [102, 97, 75],      # (Dark Yellow) 'Bareland'
            2: [61, 66, 31],       # (Dark Olive) 'Rangeland'
            3: [46, 77, 46],       # (Dark Green) 'Shrub'
            4: [56, 61, 28],       # (Dark Yellow-Green) 'Agriculture land'
            5: [54, 77, 31],       # (Dark Green) 'Tree'
            6: [89, 97, 20],       # (Dark Yellow) 'Moss and lichen'
            7: [38, 59, 49],       # (Dark Teal) 'Wet land'
            8: [16, 31, 26],       # (Very Dark Green) 'Mangrove'
            9: [22, 33, 66],       # (Dark Blue) 'Water'
            10: [82, 87, 92],      # (Dark Blue-Gray) 'Snow and ice'
            11: [46, 51, 56],      # (Dark Gray) 'Developed space'
            12: [25, 31, 43],      # (Very Dark Blue) 'Road'
            13: [56, 64, 82],      # (Dark Blue-Gray) 'Building'
            14: [102, 97, 75],     # (Dark Yellow) 'No Data'
        }

    elif color_scheme == 'grayscale':
        return {
            -99: [0, 0, 0],      # void (black)
            -30: [200, 200, 200], # 'Landmark'
            -17: [240, 240, 240], # 'plaster'
            -16: [60, 60, 60],    # 'glass'
            -15: [130, 130, 130], # 'stone'
            -14: [150, 150, 150], # 'metal'
            -13: [180, 180, 180], # 'concrete'
            -12: [170, 170, 170], # 'wood'
            -11: [70, 70, 70],    # 'brick'
            -3: [190, 190, 190],  # Building
            -2: [90, 90, 90],     # Tree
            -1: [160, 160, 160],  # Underground
            1: [230, 230, 230],   # 'Bareland'
            2: [120, 120, 120],   # 'Rangeland'
            3: [110, 110, 110],   # 'Shrub'
            4: [115, 115, 115],   # 'Agriculture land'
            5: [100, 100, 100],   # 'Tree'
            6: [210, 210, 210],   # 'Moss and lichen'
            7: [95, 95, 95],      # 'Wet land'
            8: [40, 40, 40],      # 'Mangrove'
            9: [50, 50, 50],      # 'Water'
            10: [220, 220, 220],  # 'Snow and ice'
            11: [140, 140, 140],  # 'Developed space'
            12: [30, 30, 30],     # 'Road'
            13: [170, 170, 170],  # 'Building'
            14: [230, 230, 230],  # 'No Data'
        }

    elif color_scheme == 'autumn':
        return {
            -99: [0, 0, 0],          # void
            -30: [227, 66, 52],      # (Red) 'Landmark'
            -17: [250, 240, 230],    # (Antique White) 'plaster'
            -16: [94, 33, 41],       # (Dark Red) 'glass'
            -15: [160, 120, 90],     # (Medium Brown) 'stone'
            -14: [176, 141, 87],     # (Bronze) 'metal'
            -13: [205, 186, 150],    # (Tan) 'concrete'
            -12: [204, 85, 0],       # (Dark Orange) 'wood'
            -11: [128, 55, 36],      # (Rust) 'brick'
            -3: [222, 184, 135],     # (Tan) Building
            -2: [107, 68, 35],       # (Brown) Tree
            -1: [165, 105, 79],      # (Copper) Underground
            1: [255, 235, 205],      # (Blanched Almond) 'Bareland'
            2: [133, 99, 99],        # (Brown) 'Rangeland'
            3: [139, 69, 19],        # (Saddle Brown) 'Shrub'
            4: [160, 82, 45],        # (Sienna) 'Agriculture land'
            5: [101, 67, 33],        # (Dark Brown) 'Tree'
            6: [255, 228, 196],      # (Bisque) 'Moss and lichen'
            7: [138, 51, 36],        # (Rust) 'Wet land'
            8: [85, 45, 23],         # (Deep Brown) 'Mangrove'
            9: [175, 118, 70],       # (Light Brown) 'Water'
            10: [255, 250, 240],     # (Floral White) 'Snow and ice'
            11: [188, 143, 143],     # (Rosy Brown) 'Developed space'
            12: [69, 41, 33],        # (Very Dark Brown) 'Road'
            13: [210, 180, 140],     # (Tan) 'Building'
            14: [255, 235, 205],     # (Blanched Almond) 'No Data'
        }

    elif color_scheme == 'cool':
        return {
            -99: [0, 0, 0],          # void
            -30: [180, 82, 205],     # (Purple) 'Landmark'
            -17: [240, 248, 255],    # (Alice Blue) 'plaster'
            -16: [70, 130, 180],     # (Steel Blue) 'glass'
            -15: [100, 149, 237],    # (Cornflower Blue) 'stone'
            -14: [176, 196, 222],    # (Light Steel Blue) 'metal'
            -13: [240, 255, 255],    # (Azure) 'concrete'
            -12: [65, 105, 225],     # (Royal Blue) 'wood'
            -11: [95, 158, 160],     # (Cadet Blue) 'brick'
            -3: [135, 206, 235],     # (Sky Blue) Building
            -2: [0, 128, 128],       # (Teal) Tree
            -1: [127, 255, 212],     # (Aquamarine) Underground
            1: [220, 240, 250],      # (Light Blue) 'Bareland'
            2: [72, 209, 204],       # (Medium Turquoise) 'Rangeland'
            3: [0, 191, 255],        # (Deep Sky Blue) 'Shrub'
            4: [100, 149, 237],      # (Cornflower Blue) 'Agriculture land'
            5: [0, 128, 128],        # (Teal) 'Tree'
            6: [175, 238, 238],      # (Pale Turquoise) 'Moss and lichen'
            7: [32, 178, 170],       # (Light Sea Green) 'Wet land'
            8: [25, 25, 112],        # (Midnight Blue) 'Mangrove'
            9: [30, 144, 255],       # (Dodger Blue) 'Water'
            10: [240, 255, 255],     # (Azure) 'Snow and ice'
            11: [119, 136, 153],     # (Light Slate Gray) 'Developed space'
            12: [25, 25, 112],       # (Midnight Blue) 'Road'
            13: [173, 216, 230],     # (Light Blue) 'Building'
            14: [220, 240, 250],     # (Light Blue) 'No Data'
        }

    elif color_scheme == 'earth_tones':
        return {
            -99: [0, 0, 0],          # void
            -30: [210, 105, 30],     # (Chocolate) 'Landmark'
            -17: [245, 245, 220],    # (Beige) 'plaster'
            -16: [139, 137, 137],    # (Gray) 'glass'
            -15: [160, 120, 90],     # (Medium Brown) 'stone'
            -14: [169, 169, 169],    # (Dark Gray) 'metal'
            -13: [190, 190, 180],    # (Light Gray-Tan) 'concrete'
            -12: [160, 82, 45],      # (Sienna) 'wood'
            -11: [139, 69, 19],      # (Saddle Brown) 'brick'
            -3: [210, 180, 140],     # (Tan) Building
            -2: [85, 107, 47],       # (Dark Olive Green) Tree
            -1: [133, 94, 66],       # (Beaver) Underground
            1: [222, 184, 135],      # (Burlywood) 'Bareland'
            2: [107, 142, 35],       # (Olive Drab) 'Rangeland'
            3: [85, 107, 47],        # (Dark Olive Green) 'Shrub'
            4: [128, 128, 0],        # (Olive) 'Agriculture land'
            5: [34, 139, 34],        # (Forest Green) 'Tree'
            6: [189, 183, 107],      # (Dark Khaki) 'Moss and lichen'
            7: [143, 188, 143],      # (Dark Sea Green) 'Wet land'
            8: [46, 139, 87],        # (Sea Green) 'Mangrove'
            9: [95, 158, 160],       # (Cadet Blue) 'Water'
            10: [238, 232, 205],     # (Light Tan) 'Snow and ice'
            11: [169, 169, 169],     # (Dark Gray) 'Developed space'
            12: [90, 90, 90],        # (Dark Gray) 'Road'
            13: [188, 170, 152],     # (Tan) 'Building'
            14: [222, 184, 135],     # (Burlywood) 'No Data'
        }

    elif color_scheme == 'vibrant':
        return {
            -99: [0, 0, 0],          # void
            -30: [255, 0, 255],      # (Magenta) 'Landmark'
            -17: [255, 255, 255],    # (White) 'plaster'
            -16: [0, 191, 255],      # (Deep Sky Blue) 'glass'
            -15: [255, 215, 0],      # (Gold) 'stone'
            -14: [0, 250, 154],      # (Medium Spring Green) 'metal'
            -13: [211, 211, 211],    # (Light Gray) 'concrete'
            -12: [255, 69, 0],       # (Orange Red) 'wood'
            -11: [178, 34, 34],      # (Firebrick) 'brick'
            -3: [123, 104, 238],     # (Medium Slate Blue) Building
            -2: [50, 205, 50],       # (Lime Green) Tree
            -1: [255, 20, 147],      # (Deep Pink) Underground
            1: [255, 255, 0],        # (Yellow) 'Bareland'
            2: [0, 255, 0],          # (Lime) 'Rangeland'
            3: [0, 128, 0],          # (Green) 'Shrub'
            4: [154, 205, 50],       # (Yellow Green) 'Agriculture land'
            5: [34, 139, 34],        # (Forest Green) 'Tree'
            6: [127, 255, 0],        # (Chartreuse) 'Moss and lichen'
            7: [64, 224, 208],       # (Turquoise) 'Wet land'
            8: [0, 100, 0],          # (Dark Green) 'Mangrove'
            9: [0, 0, 255],          # (Blue) 'Water'
            10: [240, 248, 255],     # (Alice Blue) 'Snow and ice'
            11: [128, 128, 128],     # (Gray) 'Developed space'
            12: [47, 79, 79],        # (Dark Slate Gray) 'Road'
            13: [135, 206, 250],     # (Light Sky Blue) 'Building'
            14: [255, 255, 224],     # (Light Yellow) 'No Data'
        }

    # ------------------------------------------------
    # NEWLY ADDED STYLISH COLOR SCHEMES BELOW:
    # ------------------------------------------------
    elif color_scheme == 'cyberpunk':
        """
        Vibrant neon purples, pinks, and blues with deep blacks.
        Think futuristic city vibes and bright neon signs.
        """
        return {
            -99: [0, 0, 0],           # void (keep it pitch black)
            -30: [255, 0, 255],       # (Neon Magenta) 'Landmark'
            -17: [255, 255, 255],     # (Bright White) 'plaster'
            -16: [0, 255, 255],       # (Neon Cyan) 'glass'
            -15: [128, 0, 128],       # (Purple) 'stone'
            -14: [50, 50, 50],        # (Dark Gray) 'metal'
            -13: [102, 0, 102],       # (Dark Magenta) 'concrete'
            -12: [255, 20, 147],      # (Deep Pink) 'wood'
            -11: [153, 0, 76],        # (Deep Purple-Red) 'brick'
            -3: [124, 0, 255],        # (Strong Neon Purple) Building
            -2: [0, 255, 153],        # (Neon Greenish Cyan) Tree
            -1: [255, 0, 102],        # (Hot Pink) Underground
            1: [255, 255, 153],       # (Pale Yellow) 'Bareland'
            2: [0, 204, 204],         # (Teal) 'Rangeland'
            3: [153, 51, 255],        # (Light Purple) 'Shrub'
            4: [0, 153, 255],         # (Bright Neon Blue) 'Agriculture land'
            5: [0, 255, 153],         # (Neon Greenish Cyan) 'Tree'
            6: [204, 0, 255],         # (Vivid Violet) 'Moss and lichen'
            7: [0, 255, 255],         # (Neon Cyan) 'Wet land'
            8: [0, 102, 102],         # (Dark Teal) 'Mangrove'
            9: [51, 0, 102],          # (Deep Indigo) 'Water'
            10: [255, 255, 255],      # (White) 'Snow and ice'
            11: [102, 102, 102],      # (Gray) 'Developed space'
            12: [0, 0, 0],            # (Black) 'Road'
            13: [204, 51, 255],       # (Bright Magenta) 'Building'
            14: [255, 255, 153],      # (Pale Yellow) 'No Data'
        }

    elif color_scheme == 'tropical':
        """
        Bold, bright 'tropical vacation' color palette.
        Lots of greens, oranges, pinks, reminiscent of island florals.
        """
        return {
            -99: [0, 0, 0],            # void
            -30: [255, 99, 164],       # (Bright Tropical Pink) 'Landmark'
            -17: [255, 248, 220],      # (Cornsilk) 'plaster'
            -16: [0, 150, 136],        # (Teal) 'glass'
            -15: [255, 140, 0],        # (Dark Orange) 'stone'
            -14: [255, 215, 180],      # (Light Peach) 'metal'
            -13: [210, 210, 210],      # (Light Gray) 'concrete'
            -12: [255, 165, 0],        # (Orange) 'wood'
            -11: [205, 92, 92],        # (Indian Red) 'brick'
            -3: [255, 193, 37],        # (Tropical Yellow) Building
            -2: [34, 139, 34],         # (Forest Green) Tree
            -1: [255, 160, 122],       # (Light Salmon) Underground
            1: [240, 230, 140],        # (Khaki) 'Bareland'
            2: [60, 179, 113],         # (Medium Sea Green) 'Rangeland'
            3: [46, 139, 87],          # (Sea Green) 'Shrub'
            4: [255, 127, 80],         # (Coral) 'Agriculture land'
            5: [50, 205, 50],          # (Lime Green) 'Tree'
            6: [255, 239, 213],        # (Papaya Whip) 'Moss and lichen'
            7: [255, 99, 71],          # (Tomato) 'Wet land'
            8: [47, 79, 79],           # (Dark Slate Gray) 'Mangrove'
            9: [0, 128, 128],          # (Teal) 'Water'
            10: [224, 255, 255],       # (Light Cyan) 'Snow and ice'
            11: [218, 112, 214],       # (Orchid) 'Developed space'
            12: [85, 107, 47],         # (Dark Olive Green) 'Road'
            13: [253, 245, 230],       # (Old Lace) 'Building'
            14: [240, 230, 140],       # (Khaki) 'No Data'
        }

    elif color_scheme == 'vintage':
        """
        A muted, old-photo or sepia-inspired palette 
        for a nostalgic or antique look.
        """
        return {
            -99: [0, 0, 0],            # void
            -30: [133, 94, 66],        # (Beaver/Brownish) 'Landmark'
            -17: [250, 240, 230],      # (Antique White) 'plaster'
            -16: [169, 157, 143],      # (Muted Brown-Gray) 'glass'
            -15: [181, 166, 127],      # (Khaki Tan) 'stone'
            -14: [120, 106, 93],       # (Faded Gray-Brown) 'metal'
            -13: [190, 172, 145],      # (Light Brown) 'concrete'
            -12: [146, 109, 83],       # (Leather Brown) 'wood'
            -11: [125, 80, 70],        # (Dusty Brick) 'brick'
            -3: [201, 174, 146],       # (Tanned Beige) Building
            -2: [112, 98, 76],         # (Faded Olive-Brown) Tree
            -1: [172, 140, 114],       # (Light Saddle Brown) Underground
            1: [222, 202, 166],        # (Light Tan) 'Bareland'
            2: [131, 114, 83],         # (Brownish) 'Rangeland'
            3: [105, 96, 74],          # (Dark Olive Brown) 'Shrub'
            4: [162, 141, 118],        # (Beige Brown) 'Agriculture land'
            5: [95, 85, 65],           # (Muted Dark Brown) 'Tree'
            6: [212, 200, 180],        # (Off-White Tan) 'Moss and lichen'
            7: [140, 108, 94],         # (Dusky Mauve-Brown) 'Wet land'
            8: [85, 73, 60],           # (Dark Taupe) 'Mangrove'
            9: [166, 152, 121],        # (Pale Brown) 'Water'
            10: [250, 245, 235],       # (Light Antique White) 'Snow and ice'
            11: [120, 106, 93],        # (Faded Gray-Brown) 'Developed space'
            12: [77, 66, 55],          # (Dark Taupe) 'Road'
            13: [203, 188, 162],       # (Light Warm Gray) 'Building'
            14: [222, 202, 166],       # (Light Tan) 'No Data'
        }

    elif color_scheme == 'neon_dreams':
        """
        A super-bright, high-energy neon palette.
        Perfect if you want a 'nightclub in 2080' vibe.
        """
        return {
            -99: [0, 0, 0],           # void
            -30: [255, 0, 255],       # (Magenta) 'Landmark'
            -17: [255, 255, 255],     # (White) 'plaster'
            -16: [0, 255, 255],       # (Cyan) 'glass'
            -15: [255, 255, 0],       # (Yellow) 'stone'
            -14: [0, 255, 0],         # (Lime) 'metal'
            -13: [128, 128, 128],     # (Gray) 'concrete'
            -12: [255, 165, 0],       # (Neon Orange) 'wood'
            -11: [255, 20, 147],      # (Deep Pink) 'brick'
            -3: [75, 0, 130],         # (Indigo) Building
            -2: [102, 255, 0],        # (Bright Lime Green) Tree
            -1: [255, 51, 153],       # (Neon Pink) Underground
            1: [255, 153, 0],         # (Bright Orange) 'Bareland'
            2: [153, 204, 0],         # (Vivid Yellow-Green) 'Rangeland'
            3: [102, 205, 170],       # (Aquamarine-ish) 'Shrub'
            4: [0, 250, 154],         # (Medium Spring Green) 'Agriculture land'
            5: [173, 255, 47],        # (Green-Yellow) 'Tree'
            6: [127, 255, 0],         # (Chartreuse) 'Moss and lichen'
            7: [64, 224, 208],        # (Turquoise) 'Wet land'
            8: [0, 128, 128],         # (Teal) 'Mangrove'
            9: [0, 0, 255],           # (Blue) 'Water'
            10: [224, 255, 255],      # (Light Cyan) 'Snow and ice'
            11: [192, 192, 192],      # (Silver) 'Developed space'
            12: [25, 25, 25],         # (Near Black) 'Road'
            13: [75, 0, 130],         # (Indigo) 'Building'
            14: [255, 153, 0],        # (Bright Orange) 'No Data'
        }

    else:
        # If an unknown color scheme is specified, return the default
        print(f"Unknown color scheme '{color_scheme}'. Using default instead.")
        return get_voxel_color_map('default')

def visualize_3d_voxel(voxel_grid, voxel_color_map = 'default', voxel_size=2.0, save_path=None):

    color_map = get_voxel_color_map(voxel_color_map)

    print("\tVisualizing 3D voxel data")
    # Create a figure and a 3D axis
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    print("\tProcessing voxels...")
    filled_voxels = voxel_grid != 0
    colors = np.zeros(voxel_grid.shape + (4,))  # RGBA

    for val in range(-99, 15):  # Updated range to include -3 and -2
        mask = voxel_grid == val
        if val in color_map:
            rgb = [x/255 for x in color_map[val]]  # Normalize RGB values to [0, 1]
            # alpha = 0.7 if ((val == -1) or (val == -2)) else 0.9  # More transparent for underground and below
            alpha = 0.0 if (val == -99) else 1
            # alpha = 1
            colors[mask] = rgb + [alpha]
        else:
            colors[mask] = [0, 0, 0, 0.9]  # Default color if not in color_map

    with tqdm(total=np.prod(voxel_grid.shape)) as pbar:
        ax.voxels(filled_voxels, facecolors=colors, edgecolors=None)
        pbar.update(np.prod(voxel_grid.shape))

    # print("Finalizing plot...")
    # Set labels and title
    # ax.set_xlabel('X')
    # ax.set_ylabel('Y')
    # ax.set_zlabel('Z (meters)')
    # ax.set_title('3D Voxel Visualization')

    # Adjust z-axis ticks to show every 10 cells or less
    z_max = voxel_grid.shape[2]
    if z_max <= 10:
        z_ticks = range(0, z_max + 1)
    else:
        z_ticks = range(0, z_max + 1, 10)
    # Remove axes
    ax.axis('off')
    # ax.set_zticks(z_ticks)
    # ax.set_zticklabels([f"{z * voxel_size:.1f}" for z in z_ticks])

    # Set aspect ratio to be equal
    max_range = np.array([voxel_grid.shape[0], voxel_grid.shape[1], voxel_grid.shape[2]]).max()
    ax.set_box_aspect((voxel_grid.shape[0]/max_range, voxel_grid.shape[1]/max_range, voxel_grid.shape[2]/max_range))

    ax.set_zlim(bottom=0)
    ax.set_zlim(top=150)

    # print("Visualization complete. Displaying plot...")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()


def visualize_3d_voxel_plotly(voxel_grid, voxel_color_map = 'default', voxel_size=2.0):

    color_map = get_voxel_color_map(voxel_color_map)

    print("Preparing visualization...")

    print("Processing voxels...")
    x, y, z = [], [], []
    i, j, k = [], [], []
    colors = []
    edge_x, edge_y, edge_z = [], [], []
    vertex_index = 0

    # Define cube faces
    cube_i = [7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2]
    cube_j = [3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3]
    cube_k = [0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6]

    with tqdm(total=np.prod(voxel_grid.shape)) as pbar:
        for xi in range(voxel_grid.shape[0]):
            for yi in range(voxel_grid.shape[1]):
                for zi in range(voxel_grid.shape[2]):
                    if voxel_grid[xi, yi, zi] != 0:
                        # Add cube vertices
                        cube_vertices = [
                            [xi, yi, zi], [xi+1, yi, zi], [xi+1, yi+1, zi], [xi, yi+1, zi],
                            [xi, yi, zi+1], [xi+1, yi, zi+1], [xi+1, yi+1, zi+1], [xi, yi+1, zi+1]
                        ]
                        x.extend([v[0] for v in cube_vertices])
                        y.extend([v[1] for v in cube_vertices])
                        z.extend([v[2] for v in cube_vertices])

                        # Add cube faces
                        i.extend([x + vertex_index for x in cube_i])
                        j.extend([x + vertex_index for x in cube_j])
                        k.extend([x + vertex_index for x in cube_k])

                        # Add color
                        color = color_map.get(voxel_grid[xi, yi, zi], [0, 0, 0])
                        colors.extend([color] * 8)

                        # Add edges
                        edges = [
                            (0,1), (1,2), (2,3), (3,0),  # Bottom face
                            (4,5), (5,6), (6,7), (7,4),  # Top face
                            (0,4), (1,5), (2,6), (3,7)   # Vertical edges
                        ]
                        for start, end in edges:
                            edge_x.extend([cube_vertices[start][0], cube_vertices[end][0], None])
                            edge_y.extend([cube_vertices[start][1], cube_vertices[end][1], None])
                            edge_z.extend([cube_vertices[start][2], cube_vertices[end][2], None])

                        vertex_index += 8
                    pbar.update(1)

    print("Creating Plotly figure...")
    mesh = go.Mesh3d(
        x=x, y=y, z=z,
        i=i, j=j, k=k,
        vertexcolor=colors,
        opacity=1,
        flatshading=True,
        name='Voxel Grid'
    )

    # Add lighting to the mesh
    mesh.update(
        lighting=dict(ambient=0.7,
                      diffuse=1,
                      fresnel=0.1,
                      specular=1,
                      roughness=0.05,
                      facenormalsepsilon=1e-15,
                      vertexnormalsepsilon=1e-15),
        lightposition=dict(x=100,
                           y=200,
                           z=0)
    )

    # Create edge lines
    edges = go.Scatter3d(
        x=edge_x, y=edge_y, z=edge_z,
        mode='lines',
        line=dict(color='lightgrey', width=1),
        name='Edges'
    )

    fig = go.Figure(data=[mesh, edges])

    # Set labels, title, and use orthographic projection
    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z (meters)',
            aspectmode='data',
            camera=dict(
                projection=dict(type="orthographic")
            )
        ),
        title='3D Voxel Visualization'
    )

    # Adjust z-axis ticks to show every 10 cells or less
    z_max = voxel_grid.shape[2]
    if z_max <= 10:
        z_ticks = list(range(0, z_max + 1))
    else:
        z_ticks = list(range(0, z_max + 1, 10))

    fig.update_layout(
        scene=dict(
            zaxis=dict(
                tickvals=z_ticks,
                ticktext=[f"{z * voxel_size:.1f}" for z in z_ticks]
            )
        )
    )

    print("Visualization complete. Displaying plot...")
    fig.show()

def plot_grid(grid, origin, adjusted_meshsize, u_vec, v_vec, transformer, vertices, data_type, vmin=None, vmax=None, color_map=None, alpha=0.5, buf=0.2, edge=True, basemap='CartoDB light', **kwargs):
    fig, ax = plt.subplots(figsize=(12, 12))

    if data_type == 'land_cover':
        land_cover_classes = kwargs.get('land_cover_classes')
        colors = [mcolors.to_rgb(f'#{r:02x}{g:02x}{b:02x}') for r, g, b in land_cover_classes.keys()]
        cmap = mcolors.ListedColormap(colors)
        norm = mcolors.BoundaryNorm(range(len(land_cover_classes)+1), cmap.N)
        title = 'Grid Cells with Dominant Land Cover Classes'
        label = 'Land Cover Class'
        tick_labels = list(land_cover_classes.values())
    elif data_type == 'building_height':
        # Create a masked array to handle special values
        masked_grid = np.ma.masked_array(grid, mask=(np.isnan(grid) | (grid == 0)))

        # Set up colormap and normalization for positive values
        cmap = plt.cm.viridis
        if vmin is None:
            vmin = np.nanmin(masked_grid[masked_grid > 0])
        if vmax is None:
            vmax = np.nanmax(masked_grid)
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

        title = 'Grid Cells with Building Heights'
        label = 'Building Height (m)'
        tick_labels = None
    elif data_type == 'dem':
        cmap = plt.cm.terrain
        if vmin is None:
            vmin = np.nanmin(grid)
        if vmax is None:
            vmax = np.nanmax(grid)
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        title = 'DEM Grid Overlaid on Map'
        label = 'Elevation (m)'
        tick_labels = None
    elif data_type == 'canopy_height':
        cmap = plt.cm.Greens
        if vmin is None:
            vmin = np.nanmin(grid)
        if vmax is None:
            vmax = np.nanmax(grid)
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        title = 'Canopy Height Grid Overlaid on Map'
        label = 'Canopy Height (m)'
        tick_labels = None
    elif data_type == 'green_view_index':
        cmap = plt.cm.Greens
        if vmin is None:
            vmin = np.nanmin(grid)
        if vmax is None:
            vmax = np.nanmax(grid)
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        title = 'Green View Index Grid Overlaid on Map'
        label = 'Green View Index'
        tick_labels = None
    elif data_type == 'sky_view_index':
        cmap = plt.cm.get_cmap('BuPu_r').copy()
        if vmin is None:
            vmin = np.nanmin(grid)
        if vmax is None:
            vmax = np.nanmax(grid)
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        title = 'Sky View Index Grid Overlaid on Map'
        label = 'Sky View Index'
        tick_labels = None
    else:
        cmap = plt.cm.viridis
        if vmin is None:
            vmin = np.nanmin(grid)
        if vmax is None:
            vmax = np.nanmax(grid)
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        tick_labels = None
        
    if color_map:
        # cmap = plt.cm.get_cmap(color_map).copy()
        cmap = sns.color_palette(color_map, as_cmap=True).copy()

    # Ensure grid is in the correct orientation
    grid = grid.T

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            cell = create_cell_polygon(origin, j, i, adjusted_meshsize, u_vec, v_vec)  # Note the swap of i and j
            x, y = cell.exterior.xy
            x, y = zip(*[transformer.transform(lon, lat) for lat, lon in zip(x, y)])

            value = grid[i, j]

            if data_type == 'building_height':
                if np.isnan(value):
                    # White fill for NaN values
                    ax.fill(x, y, alpha=alpha, fc='gray', ec='black' if edge else None, linewidth=0.1)
                elif value == 0:
                    # No fill for zero values, only edges if enabled
                    if edge:
                        ax.plot(x, y, color='black', linewidth=0.1)
                elif value > 0:
                    # Viridis colormap for positive values
                    color = cmap(norm(value))
                    ax.fill(x, y, alpha=alpha, fc=color, ec='black' if edge else None, linewidth=0.1)
            elif data_type == 'canopy_height':
                color = cmap(norm(value))
                if value == 0:
                    # No fill for zero values, only edges if enabled
                    if edge:
                        ax.plot(x, y, color='black', linewidth=0.1)
                else:
                    if edge:
                        ax.fill(x, y, alpha=alpha, fc=color, ec='black', linewidth=0.1)
                    else:
                        ax.fill(x, y, alpha=alpha, fc=color, ec=None)
            elif 'view' in data_type:
                if np.isnan(value):
                    # No fill for zero values, only edges if enabled
                    if edge:
                        ax.plot(x, y, color='black', linewidth=0.1)
                elif value >= 0:
                    # Viridis colormap for positive values
                    color = cmap(norm(value))
                    ax.fill(x, y, alpha=alpha, fc=color, ec='black' if edge else None, linewidth=0.1)
            else:
                color = cmap(norm(value))
                if edge:
                    ax.fill(x, y, alpha=alpha, fc=color, ec='black', linewidth=0.1)
                else:
                    ax.fill(x, y, alpha=alpha, fc=color, ec=None)

    crs_epsg_3857 = CRS.from_epsg(3857)

    basemaps = {
      'CartoDB dark': ctx.providers.CartoDB.DarkMatter,  # Popular dark option
      'CartoDB light': ctx.providers.CartoDB.Positron,  # Popular dark option
      'CartoDB voyager': ctx.providers.CartoDB.Voyager,  # Popular dark option
      'CartoDB light no labels': ctx.providers.CartoDB.PositronNoLabels,  # Popular dark option
      'CartoDB dark no labels': ctx.providers.CartoDB.DarkMatterNoLabels,
    }
    ctx.add_basemap(ax, crs=crs_epsg_3857, source=basemaps[basemap])
    # if basemap == "dark":
    #     ctx.add_basemap(ax, crs=crs_epsg_3857, source=ctx.providers.CartoDB.DarkMatter)
    # elif basemap == 'light':
    #     ctx.add_basemap(ax, crs=crs_epsg_3857, source=ctx.providers.CartoDB.Positron)
    # elif basemap == 'voyager':
    #     ctx.add_basemap(ax, crs=crs_epsg_3857, source=ctx.providers.CartoDB.Voyager)

    if data_type == 'building_height':
        buildings = kwargs.get('buildings', [])
        for building in buildings:
            polygon = Polygon(building['geometry']['coordinates'][0])
            x, y = polygon.exterior.xy
            x, y = zip(*[transformer.transform(lon, lat) for lat, lon in zip(x, y)])
            ax.plot(x, y, color='red', linewidth=1.5)
            # print(polygon)

    # Safe calculation of plot limits
    all_coords = np.array(vertices)
    x, y = zip(*[transformer.transform(lon, lat) for lat, lon in all_coords])

    # Calculate limits safely
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)

    if x_min != x_max and y_min != y_max and buf != 0:
        dist_x = x_max - x_min
        dist_y = y_max - y_min
        # Set limits with buffer
        ax.set_xlim(x_min - buf * dist_x, x_max + buf * dist_x)
        ax.set_ylim(y_min - buf * dist_y, y_max + buf * dist_y)
    else:
        # If coordinates are the same or buffer is 0, set limits without buffer
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)

    plt.axis('off')
    plt.tight_layout()
    plt.show()

def visualize_land_cover_grid_on_map(grid, rectangle_vertices, meshsize, source = 'Urbanwatch', vmin=None, vmax=None, alpha=0.5, buf=0.2, edge=True, basemap='CartoDB light'):

    geod = initialize_geod()

    land_cover_classes = get_land_cover_classes(source)

    vertex_0 = rectangle_vertices[0]
    vertex_1 = rectangle_vertices[1]
    vertex_3 = rectangle_vertices[3]

    dist_side_1 = calculate_distance(geod, vertex_0[1], vertex_0[0], vertex_1[1], vertex_1[0])
    dist_side_2 = calculate_distance(geod, vertex_0[1], vertex_0[0], vertex_3[1], vertex_3[0])

    side_1 = np.array(vertex_1) - np.array(vertex_0)
    side_2 = np.array(vertex_3) - np.array(vertex_0)

    u_vec = normalize_to_one_meter(side_1, dist_side_1)
    v_vec = normalize_to_one_meter(side_2, dist_side_2)

    origin = np.array(rectangle_vertices[0])
    grid_size, adjusted_meshsize = calculate_grid_size(side_1, side_2, u_vec, v_vec, meshsize)

    print(f"Calculated grid size: {grid_size}")
    # print(f"Adjusted mesh size: {adjusted_meshsize}")

    geotiff_crs = CRS.from_epsg(3857)
    transformer = setup_transformer(CRS.from_epsg(4326), geotiff_crs)

    cell_coords = create_coordinate_mesh(origin, grid_size, adjusted_meshsize, u_vec, v_vec)
    cell_coords_flat = cell_coords.reshape(2, -1).T
    transformed_coords = np.array([transform_coords(transformer, lon, lat) for lat, lon in cell_coords_flat])
    transformed_coords = transformed_coords.reshape(grid_size[::-1] + (2,))

    # print(f"Grid shape: {grid.shape}")

    plot_grid(grid, origin, adjusted_meshsize, u_vec, v_vec, transformer,
              rectangle_vertices, 'land_cover', alpha=alpha, buf=buf, edge=edge, basemap=basemap, land_cover_classes=land_cover_classes)

    unique_indices = np.unique(grid)
    unique_classes = [list(land_cover_classes.values())[i] for i in unique_indices]
    # print(f"Unique classes in the grid: {unique_classes}")

def visualize_building_height_grid_on_map(building_height_grid, filtered_buildings, rectangle_vertices, meshsize, vmin=None, vmax=None, color_map=None, alpha=0.5, buf=0.2, edge=True, basemap='CartoDB light'):
    # Calculate grid and normalize vectors
    geod = initialize_geod()
    vertex_0, vertex_1, vertex_3 = rectangle_vertices[0], rectangle_vertices[1], rectangle_vertices[3]

    dist_side_1 = calculate_distance(geod, vertex_0[1], vertex_0[0], vertex_1[1], vertex_1[0])
    dist_side_2 = calculate_distance(geod, vertex_0[1], vertex_0[0], vertex_3[1], vertex_3[0])

    side_1 = np.array(vertex_1) - np.array(vertex_0)
    side_2 = np.array(vertex_3) - np.array(vertex_0)

    u_vec = normalize_to_one_meter(side_1, dist_side_1)
    v_vec = normalize_to_one_meter(side_2, dist_side_2)

    origin = np.array(rectangle_vertices[0])
    _, adjusted_meshsize = calculate_grid_size(side_1, side_2, u_vec, v_vec, meshsize)

    # Setup transformer and plotting extent
    transformer = setup_transformer(CRS.from_epsg(4326), CRS.from_epsg(3857))

    # Plot the results
    plot_grid(building_height_grid, origin, adjusted_meshsize, u_vec, v_vec, transformer,
              rectangle_vertices, 'building_height', vmin=vmin, vmax=vmax, color_map=color_map, alpha=alpha, buf=buf, edge=edge, basemap=basemap, buildings=filtered_buildings)
    
def visualize_numerical_grid_on_map(canopy_height_grid, rectangle_vertices, meshsize, type, vmin=None, vmax=None, color_map=None, alpha=0.5, buf=0.2, edge=True, basemap='CartoDB light'):
    # Calculate grid and normalize vectors
    geod = initialize_geod()
    vertex_0, vertex_1, vertex_3 = rectangle_vertices[0], rectangle_vertices[1], rectangle_vertices[3]

    dist_side_1 = calculate_distance(geod, vertex_0[1], vertex_0[0], vertex_1[1], vertex_1[0])
    dist_side_2 = calculate_distance(geod, vertex_0[1], vertex_0[0], vertex_3[1], vertex_3[0])

    side_1 = np.array(vertex_1) - np.array(vertex_0)
    side_2 = np.array(vertex_3) - np.array(vertex_0)

    u_vec = normalize_to_one_meter(side_1, dist_side_1)
    v_vec = normalize_to_one_meter(side_2, dist_side_2)

    origin = np.array(rectangle_vertices[0])
    _, adjusted_meshsize = calculate_grid_size(side_1, side_2, u_vec, v_vec, meshsize) 

    # Setup transformer and plotting extent
    transformer = setup_transformer(CRS.from_epsg(4326), CRS.from_epsg(3857))

    # Plot the results
    plot_grid(canopy_height_grid, origin, adjusted_meshsize, u_vec, v_vec, transformer,
              rectangle_vertices, type, vmin=vmin, vmax=vmax, color_map=color_map, alpha=alpha, buf=buf, edge=edge, basemap=basemap)

def visualize_land_cover_grid(grid, mesh_size, color_map, land_cover_classes):
    all_classes = list(land_cover_classes.values())
    unique_classes = list(dict.fromkeys(all_classes))  # Preserve order and remove duplicates

    colors = [color_map[cls] for cls in unique_classes]
    cmap = mcolors.ListedColormap(colors)

    bounds = np.arange(len(unique_classes) + 1)
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    class_to_num = {cls: i for i, cls in enumerate(unique_classes)}
    numeric_grid = np.vectorize(class_to_num.get)(grid)

    plt.figure(figsize=(10, 10))
    im = plt.imshow(numeric_grid, cmap=cmap, norm=norm, interpolation='nearest')
    cbar = plt.colorbar(im, ticks=bounds[:-1] + 0.5)
    cbar.set_ticklabels(unique_classes)
    plt.title(f'Land Use/Land Cover Grid (Mesh Size: {mesh_size}m)')
    plt.xlabel('Grid Cells (X)')
    plt.ylabel('Grid Cells (Y)')
    plt.show()

def visualize_numerical_grid(grid, mesh_size, title, cmap='viridis', label='Value', vmin=None, vmax=None):
    plt.figure(figsize=(10, 10))
    plt.imshow(grid, cmap=cmap, vmin=vmin, vmax=vmax)
    plt.colorbar(label=label)
    plt.title(f'{title} (Mesh Size: {mesh_size}m)')
    plt.xlabel('Grid Cells (X)')
    plt.ylabel('Grid Cells (Y)')
    plt.show()

def convert_coordinates(coords):
    return coords

def calculate_centroid(coords):
    lat_sum = sum(coord[0] for coord in coords)
    lon_sum = sum(coord[1] for coord in coords)
    return [lat_sum / len(coords), lon_sum / len(coords)]

def calculate_center(features):
    lats = []
    lons = []
    for feature in features:
        coords = feature['geometry']['coordinates'][0]
        for lat, lon in coords:
            lats.append(lat)
            lons.append(lon)
    return sum(lats) / len(lats), sum(lons) / len(lons)

def create_circle_polygon(center_lat, center_lon, radius_meters):
    """Create a circular polygon with given center and radius"""
    # Convert radius from meters to degrees (approximate)
    radius_deg = radius_meters / 111000  # 1 degree ≈ 111km at equator
    
    # Create circle points
    points = []
    for angle in range(361):  # 0 to 360 degrees
        rad = math.radians(angle)
        lat = center_lat + (radius_deg * math.cos(rad))
        lon = center_lon + (radius_deg * math.sin(rad) / math.cos(math.radians(center_lat)))
        points.append((lat, lon))
    return Polygon(points)

def display_builing_ids_on_map(building_geojson, rectangle_vertices):
    # Parse the GeoJSON data
    geojson_data = building_geojson

    # Extract all latitudes and longitudes
    lats = [coord[0] for coord in rectangle_vertices]
    lons = [coord[1] for coord in rectangle_vertices]
    
    # Calculate center by averaging min and max values
    center_lat = (min(lats) + max(lats)) / 2
    center_lon = (min(lons) + max(lons)) / 2

    # Create circle polygon for intersection testing
    circle = create_circle_polygon(center_lat, center_lon, 200)

    # Create a map centered on the data
    m = folium.Map(location=[center_lat, center_lon], zoom_start=17)

    # Add building footprints to the map
    for feature in geojson_data:
        coords = convert_coordinates(feature['geometry']['coordinates'][0])
        building_polygon = Polygon(coords)
        
        # Check if building intersects with circle
        if building_polygon.intersects(circle):
            # Get and format building properties
            # building_id = format_building_id(feature['properties'].get('id', 0))
            building_id = str(feature['properties'].get('id', 0))
            building_name = feature['properties'].get('name:en', 
                                                    feature['properties'].get('name', f'Building {building_id}'))
            
            # Create popup content with selectable ID
            popup_content = f"""
            <div>
                Building ID: <span style="user-select: all">{building_id}</span><br>
                Name: {building_name}
            </div>
            """
            
            # Add polygon to map
            folium.Polygon(
                locations=coords,
                popup=folium.Popup(popup_content),
                color='blue',
                weight=2,
                fill=True,
                fill_color='blue',
                fill_opacity=0.2
            ).add_to(m)
            
            # Calculate centroid for label placement
            centroid = calculate_centroid(coords)
            
            # Add building ID as a selectable label
            folium.Marker(
                centroid,
                icon=folium.DivIcon(
                    html=f'''
                    <div style="
                        position: relative;
                        font-family: monospace;
                        font-size: 12px;
                        color: black;
                        background-color: rgba(255, 255, 255, 0.9);
                        padding: 5px 8px;
                        margin: -10px -15px;
                        border: 1px solid black;
                        border-radius: 4px;
                        user-select: all;
                        cursor: text;
                        white-space: nowrap;
                        display: inline-block;
                        box-shadow: 0 0 3px rgba(0,0,0,0.2);
                    ">{building_id}</div>
                    ''',
                    class_name="building-label"
                )
            ).add_to(m)

    # Save the map
    return m

def visualize_landcover_grid_on_basemap(landcover_grid, rectangle_vertices, meshsize, source='Standard', alpha=0.6, figsize=(12, 8), 
                                     basemap='CartoDB light', show_edge=False, edge_color='black', edge_width=0.5):
    """Visualizes a land cover grid GeoDataFrame using predefined color schemes.
    
    Args:
        gdf: GeoDataFrame containing grid cells with 'geometry' and 'value' columns
        source: Source of land cover classification (e.g., 'Standard', 'Urbanwatch', etc.)
        title: Title for the plot (default: None)
        alpha: Transparency of the grid overlay (default: 0.6)
        figsize: Figure size in inches (default: (12, 8))
        basemap: Basemap style (default: 'CartoDB light')
        show_edge: Whether to show cell edges (default: True)
        edge_color: Color of cell edges (default: 'black')
        edge_width: Width of cell edges (default: 0.5)
    """
    # Get land cover classes and colors
    land_cover_classes = get_land_cover_classes(source)

    gdf = grid_to_geodataframe(landcover_grid, rectangle_vertices, meshsize)
    
    # Convert RGB tuples to normalized RGB values
    colors = [(r/255, g/255, b/255) for (r,g,b) in land_cover_classes.keys()]
    
    # Create custom colormap
    cmap = ListedColormap(colors)
    
    # Create bounds for discrete colorbar
    bounds = np.arange(len(colors) + 1)
    norm = BoundaryNorm(bounds, cmap.N)
    
    # Convert to Web Mercator
    gdf_web = gdf.to_crs(epsg=3857)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot the GeoDataFrame
    gdf_web.plot(column='value',
                 ax=ax,
                 alpha=alpha,
                 cmap=cmap,
                 norm=norm,
                 legend=True,
                 legend_kwds={
                     'label': 'Land Cover Class',
                     'ticks': bounds[:-1] + 0.5,
                     'boundaries': bounds,
                     'format': lambda x, p: list(land_cover_classes.values())[int(x)]
                 },
                 edgecolor=edge_color if show_edge else 'none',
                 linewidth=edge_width if show_edge else 0)
    
    # Add basemap
    basemaps = {
        'CartoDB dark': ctx.providers.CartoDB.DarkMatter,
        'CartoDB light': ctx.providers.CartoDB.Positron,
        'CartoDB voyager': ctx.providers.CartoDB.Voyager,
        'CartoDB light no labels': ctx.providers.CartoDB.PositronNoLabels,
        'CartoDB dark no labels': ctx.providers.CartoDB.DarkMatterNoLabels,
    }
    ctx.add_basemap(ax, source=basemaps[basemap])
    
    # Set title and remove axes
    ax.set_axis_off()
    
    plt.tight_layout()
    plt.show()

def visualize_numerical_grid_on_basemap(grid, rectangle_vertices, meshsize, value_name="value", cmap='viridis', vmin=None, vmax=None, 
                                          alpha=0.6, figsize=(12, 8), basemap='CartoDB light',
                                          show_edge=False, edge_color='black', edge_width=0.5):
    """Visualizes a numerical grid GeoDataFrame (e.g., heights) on a basemap.
    
    Args:
        gdf: GeoDataFrame containing grid cells with 'geometry' and 'value' columns
        title: Title for the plot (default: None)
        cmap: Colormap to use (default: 'viridis')
        vmin: Minimum value for colormap scaling (default: None)
        vmax: Maximum value for colormap scaling (default: None)
        alpha: Transparency of the grid overlay (default: 0.6)
        figsize: Figure size in inches (default: (12, 8))
        basemap: Basemap style (default: 'CartoDB light')
        show_edge: Whether to show cell edges (default: True)
        edge_color: Color of cell edges (default: 'black')
        edge_width: Width of cell edges (default: 0.5)
    """

    gdf = grid_to_geodataframe(grid, rectangle_vertices, meshsize)

    # Convert to Web Mercator
    gdf_web = gdf.to_crs(epsg=3857)
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot the GeoDataFrame
    gdf_web.plot(column='value',
                 ax=ax,
                 alpha=alpha,
                 cmap=cmap,
                 vmin=vmin,
                 vmax=vmax,
                 legend=True,
                 legend_kwds={'label': value_name},
                 edgecolor=edge_color if show_edge else 'none',
                 linewidth=edge_width if show_edge else 0)
    
    # Add basemap
    basemaps = {
        'CartoDB dark': ctx.providers.CartoDB.DarkMatter,
        'CartoDB light': ctx.providers.CartoDB.Positron,
        'CartoDB voyager': ctx.providers.CartoDB.Voyager,
        'CartoDB light no labels': ctx.providers.CartoDB.PositronNoLabels,
        'CartoDB dark no labels': ctx.providers.CartoDB.DarkMatterNoLabels,
    }
    ctx.add_basemap(ax, source=basemaps[basemap])
    
    # Set title and remove axes
    ax.set_axis_off()
    
    plt.tight_layout()
    plt.show()

def visualize_numerical_gdf_on_basemap(gdf, value_name="value", cmap='viridis', vmin=None, vmax=None,
                            alpha=0.6, figsize=(12, 8), basemap='CartoDB light',
                            show_edge=False, edge_color='black', edge_width=0.5):
    """Visualizes a GeoDataFrame with numerical values on a basemap.
    
    Args:
        gdf: GeoDataFrame containing grid cells with 'geometry' and 'value' columns
        value_name: Name of the value column and legend label (default: "value")
        cmap: Colormap to use (default: 'viridis')
        vmin: Minimum value for colormap scaling (default: None)
        vmax: Maximum value for colormap scaling (default: None)
        alpha: Transparency of the grid overlay (default: 0.6)
        figsize: Figure size in inches (default: (12, 8))
        basemap: Basemap style (default: 'CartoDB light')
        show_edge: Whether to show cell edges (default: False)
        edge_color: Color of cell edges (default: 'black')
        edge_width: Width of cell edges (default: 0.5)
    """
    # Convert to Web Mercator if not already in that CRS
    if gdf.crs != 'EPSG:3857':
        gdf_web = gdf.to_crs(epsg=3857)
    else:
        gdf_web = gdf
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot the GeoDataFrame
    gdf_web.plot(column=value_name,
                 ax=ax,
                 alpha=alpha,
                 cmap=cmap,
                 vmin=vmin,
                 vmax=vmax,
                 legend=True,
                 legend_kwds={'label': value_name},
                 edgecolor=edge_color if show_edge else 'none',
                 linewidth=edge_width if show_edge else 0)
    
    # Add basemap
    basemaps = {
        'CartoDB dark': ctx.providers.CartoDB.DarkMatter,
        'CartoDB light': ctx.providers.CartoDB.Positron,
        'CartoDB voyager': ctx.providers.CartoDB.Voyager,
        'CartoDB light no labels': ctx.providers.CartoDB.PositronNoLabels,
        'CartoDB dark no labels': ctx.providers.CartoDB.DarkMatterNoLabels,
    }
    ctx.add_basemap(ax, source=basemaps[basemap])
    
    # Set title and remove axes
    ax.set_axis_off()
    
    plt.tight_layout()
    plt.show()

def visualize_point_gdf_on_basemap(point_gdf, value_name='value', **kwargs):
    """Visualizes a point GeoDataFrame on a basemap with colors based on values.
    
    Args:
        point_gdf: GeoDataFrame with point geometries and values
        value_name: Name of the column containing values to visualize (default: 'value')
        **kwargs: Optional visualization parameters including:
            - figsize: Tuple for figure size (default: (12, 8))
            - colormap: Matplotlib colormap name (default: 'viridis')
            - markersize: Size of points (default: 20)
            - alpha: Transparency of points (default: 0.7)
            - vmin: Minimum value for colormap scaling (default: None)
            - vmax: Maximum value for colormap scaling (default: None)
            - title: Plot title (default: None)
            - basemap_style: Contextily basemap style (default: CartoDB.Positron)
            - zoom: Basemap zoom level (default: 15)
            
    Returns:
        matplotlib figure and axis objects
    """
    import matplotlib.pyplot as plt
    import contextily as ctx
    
    # Set default parameters
    defaults = {
        'figsize': (12, 8),
        'colormap': 'viridis',
        'markersize': 20,
        'alpha': 0.7,
        'vmin': None,
        'vmax': None,
        'title': None,
        'basemap_style': ctx.providers.CartoDB.Positron,
        'zoom': 15
    }
    
    # Update defaults with provided kwargs
    settings = {**defaults, **kwargs}
    
    # Create figure and axis
    fig, ax = plt.subplots(figsize=settings['figsize'])
    
    # Convert to Web Mercator for basemap compatibility
    point_gdf_web = point_gdf.to_crs(epsg=3857)
    
    # Plot points
    scatter = point_gdf_web.plot(
        column=value_name,
        ax=ax,
        cmap=settings['colormap'],
        markersize=settings['markersize'],
        alpha=settings['alpha'],
        vmin=settings['vmin'],
        vmax=settings['vmax'],
        legend=True,
        legend_kwds={
            'label': value_name,
            'orientation': 'vertical',
            'shrink': 0.8
        }
    )
    
    # Add basemap
    ctx.add_basemap(
        ax,
        source=settings['basemap_style'],
        zoom=settings['zoom']
    )
    
    # Set title if provided
    if settings['title']:
        plt.title(settings['title'])
    
    # Remove axes
    ax.set_axis_off()
    
    # Adjust layout to prevent colorbar cutoff
    plt.tight_layout()
    plt.show()

def create_multi_view_scene(meshes, output_directory="output", projection_type="perspective", distance_factor=1.0):
    """
    Create multiple views of the scene from different angles.
    
    Args:
        meshes: Dictionary of meshes to visualize
        output_directory: Directory to save output images
        projection_type: Either "perspective" or "orthographic" (default: "perspective")
    """
    # Compute overall bounding box across all meshes
    vertices_list = [mesh.vertices for mesh in meshes.values()]
    all_vertices = np.vstack(vertices_list)
    bbox = np.array([
        [all_vertices[:, 0].min(), all_vertices[:, 1].min(), all_vertices[:, 2].min()],
        [all_vertices[:, 0].max(), all_vertices[:, 1].max(), all_vertices[:, 2].max()]
    ])

    # Compute the center and diagonal of the bounding box
    center = (bbox[1] + bbox[0]) / 2
    diagonal = np.linalg.norm(bbox[1] - bbox[0])

    # Adjust distance based on projection type
    if projection_type.lower() == "orthographic":
        distance = diagonal * 5  # Increase distance for orthographic to capture full scene
    else:
        distance = diagonal * 1.8 * distance_factor  # Original distance for perspective

    # Define the isometric viewing angles
    iso_angles = {
        'iso_front_right': (1, 1, 0.7),
        'iso_front_left': (-1, 1, 0.7),
        'iso_back_right': (1, -1, 0.7),
        'iso_back_left': (-1, -1, 0.7)
    }

    # Compute camera positions for isometric views
    camera_positions = {}
    for name, direction in iso_angles.items():
        direction = np.array(direction)
        direction = direction / np.linalg.norm(direction)
        camera_pos = center + direction * distance
        camera_positions[name] = [camera_pos, center, (0, 0, 1)]

    # Add orthographic views
    ortho_views = {
        'xy_top': [center + np.array([0, 0, distance]), center, (-1, 0, 0)],
        'yz_right': [center + np.array([distance, 0, 0]), center, (0, 0, 1)],
        'xz_front': [center + np.array([0, distance, 0]), center, (0, 0, 1)],
        'yz_left': [center + np.array([-distance, 0, 0]), center, (0, 0, 1)],
        'xz_back': [center + np.array([0, -distance, 0]), center, (0, 0, 1)]
    }
    camera_positions.update(ortho_views)

    images = []
    for view_name, camera_pos in camera_positions.items():
        # Create new plotter for each view
        plotter = pv.Plotter(notebook=True, off_screen=True)
        
        # Set the projection type
        if projection_type.lower() == "orthographic":
            plotter.enable_parallel_projection()
            # Set parallel scale to ensure the whole scene is visible
            plotter.camera.parallel_scale = diagonal * 0.4 * distance_factor  # Adjust this factor as needed

        elif projection_type.lower() != "perspective":
            print(f"Warning: Unknown projection_type '{projection_type}'. Using perspective projection.")

        # Add each mesh to the scene
        for class_id, mesh in meshes.items():
            vertices = mesh.vertices
            faces = np.hstack([[3, *face] for face in mesh.faces])
            pv_mesh = pv.PolyData(vertices, faces)

            if hasattr(mesh.visual, 'face_colors'):
                colors = mesh.visual.face_colors
                if colors.max() > 1:
                    colors = colors / 255.0
                pv_mesh.cell_data['colors'] = colors

            plotter.add_mesh(pv_mesh,
                           rgb=True,
                           scalars='colors' if hasattr(mesh.visual, 'face_colors') else None)

        # Set camera position for this view
        plotter.camera_position = camera_pos

        # Save screenshot
        filename = f'{output_directory}/city_view_{view_name}.png'
        plotter.screenshot(filename)
        images.append((view_name, filename))
        plotter.close()

    return images

def visualize_voxcity_multi_view(voxel_array, meshsize, **kwargs):
    """
    Create multiple views of the voxel city data.
    """

    os.system('Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &')
    os.environ['DISPLAY'] = ':99'

    # Configure PyVista settings
    pv.set_plot_theme('document')
    pv.global_theme.background = 'white'
    pv.global_theme.window_size = [1024, 768]
    pv.global_theme.jupyter_backend = 'static'
    
    # Parse kwargs
    voxel_color_map = kwargs.get("voxel_color_map", 'default')
    vox_dict = get_voxel_color_map(voxel_color_map)
    output_directory = kwargs.get("output_directory", 'output')
    base_filename = kwargs.get("output_file_name", None)
    sim_grid = kwargs.get("sim_grid", None)
    dem_grid_ori = kwargs.get("dem_grid", None)
    if dem_grid_ori is not None:
        dem_grid = dem_grid_ori - np.min(dem_grid_ori)
    z_offset = kwargs.get("view_point_height", 1.5)
    cmap_name = kwargs.get("colormap", "viridis")
    vmin = kwargs.get("vmin", np.nanmin(sim_grid))
    vmax = kwargs.get("vmax", np.nanmax(sim_grid))
    projection_type = kwargs.get("projection_type", "perspective")
    distance_factor = kwargs.get("distance_factor", 1.0)
    save_obj = kwargs.get("save_obj", False)
    show_views = kwargs.get("show_views", True)

    # Create meshes
    print("Creating voxel meshes...")
    meshes = create_city_meshes(voxel_array, vox_dict, meshsize=meshsize)

    # Create sim_grid surface mesh if provided
    if sim_grid is not None and dem_grid is not None:
        print("Creating sim_grid surface mesh...")
        sim_mesh = create_sim_surface_mesh(
            sim_grid, dem_grid,
            meshsize=meshsize,
            z_offset=z_offset,
            cmap_name=cmap_name,
            vmin=vmin,
            vmax=vmax
        )
        if sim_mesh is not None:
            meshes["sim_surface"] = sim_mesh
            # If vmin/vmax not provided, use actual min/max of the valid sim data
            
        # Prepare the colormap and create colorbar
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        scalar_map = cm.ScalarMappable(norm=norm, cmap=cmap_name)
        
        # Create a figure and axis for the colorbar but don't display
        fig, ax = plt.subplots(figsize=(6, 1))
        plt.colorbar(scalar_map, cax=ax, orientation='horizontal')
        plt.tight_layout()
        plt.show()

    # Export if filename provided
    if base_filename is not None:
        print(f"Exporting files to '{base_filename}.*' ...")# Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        export_meshes(meshes, output_directory, base_filename)

    if show_views:  
        # Create and save multiple views
        print("Creating multiple views...")        
        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        image_files = create_multi_view_scene(meshes, output_directory=output_directory, projection_type=projection_type, distance_factor=distance_factor)

        # Display each view separately
        for view_name, img_file in image_files:
            plt.figure(figsize=(12, 8))
            img = plt.imread(img_file)
            plt.imshow(img)
            plt.title(view_name.replace('_', ' ').title(), pad=20)
            plt.axis('off')
            plt.show()
            plt.close()
    
        # After creating the meshes and before visualization
    if save_obj:
        output_directory = kwargs.get('output_directory', 'output')
        output_file_name = kwargs.get('output_file_name', 'voxcity_mesh')
        obj_path, mtl_path = save_obj_from_colored_mesh(meshes, output_directory, output_file_name)
        print(f"Saved mesh files to:\n  {obj_path}\n  {mtl_path}")

def visualize_voxcity_multi_view_with_multiple_sim_grids(voxel_array, meshsize, sim_configs, **kwargs):
    """
    Create multiple views of the voxel city data with multiple simulation grids.
    
    Args:
        voxel_array: 3D numpy array containing voxel data
        meshsize: Size of each voxel/cell
        sim_configs: List of dictionaries, each containing configuration for a simulation grid:
            {
                'sim_grid': 2D numpy array of simulation values,
                'z_offset': height offset in meters (default: 1.5),
                'cmap_name': colormap name (default: 'viridis'),
                'vmin': minimum value for colormap (optional),
                'vmax': maximum value for colormap (optional),
                'label': label for the colorbar (optional)
            }
        **kwargs: Additional arguments including:
            - vox_dict: Dictionary mapping voxel values to colors
            - output_directory: Directory to save output images
            - output_file_name: Base filename for exports
            - dem_grid: DEM grid for height information
            - projection_type: 'perspective' or 'orthographic'
            - distance_factor: Factor to adjust camera distance
    """
    os.system('Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &')
    os.environ['DISPLAY'] = ':99'

    # Configure PyVista settings
    pv.set_plot_theme('document')
    pv.global_theme.background = 'white'
    window_width = kwargs.get("window_width", 1024)
    window_height = kwargs.get("window_height", 768)
    pv.global_theme.window_size = [window_width, window_height]
    pv.global_theme.jupyter_backend = 'static'

    # Parse general kwargs
    voxel_color_map = kwargs.get("voxel_color_map", 'default')
    vox_dict = get_voxel_color_map(voxel_color_map)
    output_directory = kwargs.get("output_directory", 'output')
    base_filename = kwargs.get("output_file_name", None)
    dem_grid_ori = kwargs.get("dem_grid", None)
    projection_type = kwargs.get("projection_type", "perspective")
    distance_factor = kwargs.get("distance_factor", 1.0)
    show_views = kwargs.get("show_views", True)
    save_obj = kwargs.get("save_obj", False)

    if dem_grid_ori is not None:
        dem_grid = dem_grid_ori - np.min(dem_grid_ori)
    
    # Create meshes
    print("Creating voxel meshes...")
    meshes = create_city_meshes(voxel_array, vox_dict, meshsize=meshsize)

    # Process each simulation grid
    for i, config in enumerate(sim_configs):
        sim_grid = config['sim_grid']
        if sim_grid is None or dem_grid is None:
            continue

        z_offset = config.get('z_offset', 1.5)
        cmap_name = config.get('cmap_name', 'viridis')
        vmin = config.get('vmin', np.nanmin(sim_grid))
        vmax = config.get('vmax', np.nanmax(sim_grid))
        label = config.get('label', f'Simulation {i+1}')

        print(f"Creating sim_grid surface mesh for {label}...")
        sim_mesh = create_sim_surface_mesh(
            sim_grid, dem_grid,
            meshsize=meshsize,
            z_offset=z_offset,
            cmap_name=cmap_name,
            vmin=vmin,
            vmax=vmax
        )
        
        if sim_mesh is not None:
            meshes[f"sim_surface_{i}"] = sim_mesh
            
            # Create colorbar for this simulation
            norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
            scalar_map = cm.ScalarMappable(norm=norm, cmap=cmap_name)
            
            fig, ax = plt.subplots(figsize=(6, 1))
            plt.colorbar(scalar_map, cax=ax, orientation='horizontal', label=label)
            plt.tight_layout()
            plt.show()

    # Export if filename provided
    if base_filename is not None:
        print(f"Exporting files to '{base_filename}.*' ...")
        os.makedirs(output_directory, exist_ok=True)
        export_meshes(meshes, output_directory, base_filename)

    if show_views:
        # Create and save multiple views
        print("Creating multiple views...")        
        os.makedirs(output_directory, exist_ok=True)
        image_files = create_multi_view_scene(
            meshes, 
            output_directory=output_directory,
            projection_type=projection_type,
            distance_factor=distance_factor
        )

        # Display each view separately
        for view_name, img_file in image_files:
            plt.figure(figsize=(12, 8))
            img = plt.imread(img_file)
            plt.imshow(img)
            plt.title(view_name.replace('_', ' ').title(), pad=20)
            plt.axis('off')
            plt.show()
            plt.close()

    # After creating the meshes and before visualization
    if save_obj:
        output_directory = kwargs.get('output_directory', 'output')
        output_file_name = kwargs.get('output_file_name', 'voxcity_mesh')
        obj_path, mtl_path = save_obj_from_colored_mesh(meshes, output_directory, output_file_name)
        print(f"Saved mesh files to:\n  {obj_path}\n  {mtl_path}")

def visualize_voxcity_with_sim_meshes(voxel_array, meshsize, custom_meshes=None, **kwargs):
    """
    Create multiple views of the voxel city data with custom simulation meshes replacing specific voxel classes.
    
    Parameters
    ----------
    voxel_array : np.ndarray
        3D array of voxel values.
    meshsize : float
        Size of each voxel in meters.
    custom_meshes : dict, optional
        Dictionary mapping voxel class IDs to custom meshes (e.g., {-3: building_svf_mesh}).
        These meshes will replace the original voxel meshes for visualization.
    **kwargs:
        vox_dict : dict
            Dictionary mapping voxel class IDs to colors.
        output_directory : str
            Directory to save output files.
        output_file_name : str
            Base filename for exported meshes.
        sim_grid : np.ndarray
            2D array with simulation values to visualize as a surface.
        dem_grid : np.ndarray
            2D array with elevation values.
        view_point_height : float
            Height offset for simulation grid visualization.
        colormap : str
            Matplotlib colormap name for simulation results.
        vmin, vmax : float
            Min/max values for color mapping.
        projection_type : str
            'perspective' or 'orthogonal'
        distance_factor : float
            Adjusts camera distance.
        colorbar_title : str
            Title for the colorbar (for simulation results).
        value_name : str
            Name of the field in metadata containing values to visualize.
        nan_color : str or tuple
            Color to use for NaN values (default: 'gray')
    
    Returns
    -------
    list
        List of (view_name, image_file_path) tuples for the generated views.
    """
    os.system('Xvfb :99 -screen 0 1024x768x24 > /dev/null 2>&1 &')
    os.environ['DISPLAY'] = ':99'

    # Configure PyVista settings
    pv.set_plot_theme('document')
    pv.global_theme.background = 'white'
    window_width = kwargs.get("window_width", 1024)
    window_height = kwargs.get("window_height", 768)
    pv.global_theme.window_size = [window_width, window_height]
    pv.global_theme.jupyter_backend = 'static'
    
    # Parse kwargs
    voxel_color_map = kwargs.get("voxel_color_map", 'default')
    vox_dict = get_voxel_color_map(voxel_color_map)
    output_directory = kwargs.get("output_directory", 'output')
    base_filename = kwargs.get("output_file_name", None)
    sim_grid = kwargs.get("sim_grid", None)
    dem_grid_ori = kwargs.get("dem_grid", None)
    if dem_grid_ori is not None:
        dem_grid = dem_grid_ori - np.min(dem_grid_ori)
    z_offset = kwargs.get("view_point_height", 1.5)
    cmap_name = kwargs.get("colormap", "viridis")
    vmin = kwargs.get("vmin", None)
    vmax = kwargs.get("vmax", None)
    projection_type = kwargs.get("projection_type", "perspective")
    distance_factor = kwargs.get("distance_factor", 1.0)
    colorbar_title = kwargs.get("colorbar_title", "")
    value_name = kwargs.get("value_name", None)
    nan_color = kwargs.get("nan_color", "gray")
    show_views = kwargs.get("show_views", True)
    save_obj = kwargs.get("save_obj", False)
    
    if value_name is None:
        print("Set value_name")

    # Create meshes from voxel data
    print("Creating voxel meshes...")
    meshes = create_city_meshes(voxel_array, vox_dict, meshsize=meshsize)
    
    # Replace specific voxel class meshes with custom simulation meshes
    if custom_meshes is not None:
        for class_id, custom_mesh in custom_meshes.items():
            # Apply coloring to custom meshes if they have metadata values
            if hasattr(custom_mesh, 'metadata') and value_name in custom_mesh.metadata:
                # Create a colored copy of the mesh for visualization
                import matplotlib.cm as cm
                import matplotlib.colors as mcolors
                
                # Get values from metadata
                values = custom_mesh.metadata[value_name]
                
                # Set vmin/vmax if not provided
                local_vmin = vmin if vmin is not None else np.nanmin(values[~np.isnan(values)])
                local_vmax = vmax if vmax is not None else np.nanmax(values[~np.isnan(values)])

                # Create colors
                cmap = cm.get_cmap(cmap_name)
                norm = mcolors.Normalize(vmin=local_vmin, vmax=local_vmax)
                
                # Handle NaN values with custom color
                face_colors = np.zeros((len(values), 4))
                
                # Convert string color to RGBA if needed
                if isinstance(nan_color, str):
                    import matplotlib.colors as mcolors
                    nan_rgba = np.array(mcolors.to_rgba(nan_color))
                else:
                    # Assume it's already a tuple/list of RGBA values
                    nan_rgba = np.array(nan_color)
                
                # Apply colors: NaN values get nan_color, others get colormap colors
                nan_mask = np.isnan(values)
                face_colors[~nan_mask] = cmap(norm(values[~nan_mask]))
                face_colors[nan_mask] = nan_rgba
                
                # Create a copy with colors
                vis_mesh = custom_mesh.copy()
                vis_mesh.visual.face_colors = face_colors

                # Prepare the colormap and create colorbar
                norm = mcolors.Normalize(vmin=local_vmin, vmax=local_vmax)
                scalar_map = cm.ScalarMappable(norm=norm, cmap=cmap_name)
                
                # Create a figure and axis for the colorbar but don't display
                fig, ax = plt.subplots(figsize=(6, 1))
                cbar = plt.colorbar(scalar_map, cax=ax, orientation='horizontal')
                if colorbar_title:
                    cbar.set_label(colorbar_title)
                plt.tight_layout()
                plt.show()  
                
                if class_id in meshes:
                    print(f"Replacing voxel class {class_id} with colored custom simulation mesh")
                    meshes[class_id] = vis_mesh
                else:
                    print(f"Adding colored custom simulation mesh for class {class_id}")
                    meshes[class_id] = vis_mesh
            else:
                # No metadata values, use the mesh as is
                if class_id in meshes:
                    print(f"Replacing voxel class {class_id} with custom simulation mesh")
                    meshes[class_id] = custom_mesh
                else:
                    print(f"Adding custom simulation mesh for class {class_id}")
                    meshes[class_id] = custom_mesh

    # Create sim_grid surface mesh if provided
    if sim_grid is not None and dem_grid is not None:
        print("Creating sim_grid surface mesh...")
        
        # If vmin/vmax not provided, use actual min/max of the valid sim data
        if vmin is None:
            vmin = np.nanmin(sim_grid)
        if vmax is None:
            vmax = np.nanmax(sim_grid)
            
        sim_mesh = create_sim_surface_mesh(
            sim_grid, dem_grid,
            meshsize=meshsize,
            z_offset=z_offset,
            cmap_name=cmap_name,
            vmin=vmin,
            vmax=vmax,
            nan_color=nan_color  # Pass nan_color to the mesh creation
        )
        if sim_mesh is not None:
            meshes["sim_surface"] = sim_mesh
            
        # # Prepare the colormap and create colorbar
        # norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
        # scalar_map = cm.ScalarMappable(norm=norm, cmap=cmap_name)
        
        # # Create a figure and axis for the colorbar but don't display
        # fig, ax = plt.subplots(figsize=(6, 1))
        # cbar = plt.colorbar(scalar_map, cax=ax, orientation='horizontal')
        # if colorbar_title:
        #     cbar.set_label(colorbar_title)
        # plt.tight_layout()
        # plt.show()

    # Export if filename provided
    if base_filename is not None:
        print(f"Exporting files to '{base_filename}.*' ...")
        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)
        export_meshes(meshes, output_directory, base_filename)

 
    # Create and save multiple views
    print("Creating multiple views...")        
    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    if show_views:
        image_files = create_multi_view_scene(meshes, output_directory=output_directory, 
                                         projection_type=projection_type, 
                                         distance_factor=distance_factor)

        # Display each view separately
        for view_name, img_file in image_files:
            plt.figure(figsize=(24, 16))
            img = plt.imread(img_file)
            plt.imshow(img)
            plt.title(view_name.replace('_', ' ').title(), pad=20)
            plt.axis('off')
            plt.show()
            plt.close()
        
    # After creating the meshes and before visualization
    if save_obj:
        output_directory = kwargs.get('output_directory', 'output')
        output_file_name = kwargs.get('output_file_name', 'voxcity_mesh')
        obj_path, mtl_path = save_obj_from_colored_mesh(meshes, output_directory, output_file_name)
        print(f"Saved mesh files to:\n  {obj_path}\n  {mtl_path}")    

def visualize_building_sim_results(voxel_array, meshsize, building_sim_mesh, **kwargs):
    """
    Visualize building simulation results by replacing building meshes in the original model.
    
    This is a specialized wrapper around visualize_voxcity_with_sim_meshes that specifically
    targets building simulation meshes (assuming building class ID is -3).
    
    Parameters
    ----------
    voxel_array : np.ndarray
        3D array of voxel values.
    meshsize : float
        Size of each voxel in meters.
    building_sim_mesh : trimesh.Trimesh
        Simulation result mesh for buildings with values stored in metadata.
    **kwargs:
        Same parameters as visualize_voxcity_with_sim_meshes.
        Additional parameters:
        value_name : str
            Name of the field in metadata containing values to visualize (default: 'svf_values')
        nan_color : str or tuple
            Color for NaN values (default: 'gray')
        
    Returns
    -------
    list
        List of (view_name, image_file_path) tuples for the generated views.
    """
    # Building class ID is typically -3 in voxcity
    building_class_id = kwargs.get("building_class_id", -3)
    
    # Create custom meshes dictionary with the building simulation mesh
    custom_meshes = {building_class_id: building_sim_mesh}
    
    # Add colorbar title if not provided
    if "colorbar_title" not in kwargs:
        # Try to guess a title based on the mesh name/type
        if hasattr(building_sim_mesh, 'name') and building_sim_mesh.name:
            kwargs["colorbar_title"] = building_sim_mesh.name
        else:
            # Use value_field name as fallback
            value_name = kwargs.get("value_name", "svf_values")
            pretty_name = value_name.replace('_', ' ').title()
            kwargs["colorbar_title"] = pretty_name
    
    # Call the more general visualization function
    visualize_voxcity_with_sim_meshes(
        voxel_array,
        meshsize,
        custom_meshes=custom_meshes,
        **kwargs
    )