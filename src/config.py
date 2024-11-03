from pathlib import Path

# Define marker sizes, in mm
MARKER_SIZES = [75,65,37,23]

# Define paths to csv files, containing data to visualize
DIR_PATH = Path.cwd()
ARUCO_CENTERS_ANGLES_COMPARISON_PATH =  DIR_PATH / Path(r'src\data\aruco_centers_angles.csv')
ARUCO_CENTERS_VS_CORNERS_COMPARISON_PATH = DIR_PATH / Path(r'src\data\aruco_centers_vs_corners.csv')
QRCODES_MARKER_SIZES_COMPARISON_PATH = DIR_PATH / Path(r'src\data\Qrcode_marker_sizes.csv')
ARUCO_QRCODES_COMPARISON_PATH = DIR_PATH / Path(r'src\data\Qrcode_vs_aruco.csv')

# Define colors
COLORS = ['blue', 'orange', 'green', 'purple']
BG_COLORS = ['white', 'lightgray', 'silver', 'darkgray', 'gray']