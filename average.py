"""这个文件用于计算每年海平面平均并输出到year_average文件夹
输出为csv格式，不保留行索引，读出时直接read_csv()即可
"""

import netCDF4 as nc
import numpy as npy
import pandas as pd

ROOT = "./v4b/"
FILE_NAME = "SEA_SURFACE_HEIGHT_mon_mean_{0}-{1}_ECCO_V4r4b_latlon_0p50deg.nc"

for i in range(1992, 2018):

    val_12 = nc.Dataset("./rain_nc/"+str(i)+"09.nc").variables["precipitation"][:]
    val_1 = nc.Dataset("./rain_nc/"+str(i)+"10.nc").variables["precipitation"][:]
    val_2 = nc.Dataset("./rain_nc/"+str(i)+"11.nc").variables["precipitation"][:]

    val = (val_12+val_1+val_2)/3.0

    df = pd.DataFrame(npy.squeeze(val.data))
    df.to_csv("./precipitation_season_average/fall/{}.csv".format(i), index=0)