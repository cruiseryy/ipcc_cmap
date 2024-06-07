from matplotlib.colors import LinearSegmentedColormap
import numpy as np
import pandas as pd
import math

# author: cruiseryy 20240607
# i did not create the color maps but i wrote a script to convert them to matplotlib colormaps
# source = https://github.com/IPCC-WG1/colormaps/tree/master/discrete_colormaps_rgb_0-255
# the excel file is also included in the repository
# feel free to use, modify, and distribute the code

class ipcc_cmap: 
    def __init__(self, file_path = 'ipcc_disc_cmaps.xlsx'):
        self.file_path = file_path
        return
    
    def read_rgb_data_from_excel(self):
        self.CMAP = {}
        xl = pd.ExcelFile(self.file_path)

        for sheet_name in xl.sheet_names:
            df = xl.parse(sheet_name, header = None)
            df = df.dropna(how='all')

            current_header = None
            color_data = []

            for index, row in df.iterrows():
                if math.isnan(row[1]):
                    if current_header is not None:
                        self.CMAP[current_header] = color_data
                    color_data = []
                    current_header = row[0]
                else:
                    try:
                        rgb = list(row)
                        color_data.append(rgb)
                    except ValueError:
                        continue

            if current_header is not None:
                self.CMAP[current_header] = color_data

        return self.CMAP
    
    # type:
    # 'div' (divergence)
    # 'seq' (sequential)
    # var: 
    # 'prec' (precipitation)
    # 'temp' (temperature)
    # 'wind' (wind speed)
    # 'cryo' (cryosphere)
    # 'chem' (CO2/CH4/aerosals)
    # 'slev' (sea level)
    # 'misc' (miscellaneous) (e.g., misc_seq_{1,2,3}_levels)
    # levels:
    # 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
    def get_ipcc_cmap(self, type_ = 'div', var_ = 'prec', levels = 10, reverse = False):

        key_ = f"{var_}_{type_}_{levels}"
        rgb = self.CMAP[key_]

        if reverse:
            rgb = rgb[::-1]

        rgb_normalized = np.array(rgb) / 255.0
        custom_colormap = LinearSegmentedColormap.from_list("Custom_Colormap", rgb_normalized)
        
        return custom_colormap

if __name__  == '__main__':
    tmp = ipcc_cmap()
    tmp.read_rgb_data_from_excel()
    cmap = tmp.get_ipcc_cmap(type_ = 'div', var_ = 'prec', levels = 10, reverse = False)