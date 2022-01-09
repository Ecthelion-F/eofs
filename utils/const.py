"""
===========
常用常量模块
===========
"""

import netCDF4 as nc
from numpy import array

# 遍历数据集需要用到的常量
ROOT = "./v4b/"
FILE_NAME = "SEA_SURFACE_HEIGHT_mon_mean_{0}-{1}_ECCO_V4r4b_latlon_0p50deg.nc"


# SSH数据集经纬度常量
_REFERENCE_FILE = "01.nc"
with nc.Dataset(_REFERENCE_FILE) as _reference_nc:
    LONS = _reference_nc.variables['longitude'][:]
    LATS = _reference_nc.variables['latitude'][:]


# 降水数据集经纬度常量
_REFERENCE_FILE_PREC = "199201.nc"
with nc.Dataset(_REFERENCE_FILE_PREC) as _reference_nc:
    LONS_PREC = _reference_nc.variables['lon'][:]
    LATS_PREC = _reference_nc.variables['lat'][:]


# 厄尔尼诺年和拉尼娜年列表
YEAR_E = array([1994, 1997, 2002, 2004, 2006, 2009, 2014])
YEAR_L = array([1995, 1998, 1999, 2000, 2007, 2010, 2011])