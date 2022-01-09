"""
========
常用工具函数模块，意在简化编码，专注于数据分析
========
"""

import cmaps
from eofs.standard import Eof
import matplotlib.pyplot as plt
from mpl_toolkits.basemap  import Basemap
import netCDF4 as nc
import numpy as npy
import pandas as pd

_CROPED_MASK_SSH = pd.read_csv("croped_mask.csv")
_CROPED_MASK_PREC = pd.read_csv("croped_mask_china_land.csv")


def convert_date(year, month):
    """没啥用的日期字符串转换工具，传入年月，传回字符串式的年月，主要是月有前导0
    遍历数据集的时候有用
    """
    y = str(year)
    m = str(month) if month>=10 else "0"+str(month)
    return y, m


def plot_to_map(lons, lats, data, lat_0=0, lon_0=160, 
                low_lon=100, low_lat=-20, up_lon=320, up_lat=20,
                fig_title="TITLE", set_cmaps=None):
    """一个把抄来的代码抽象掉的函数

        Attributes:
        ----
            lons,lats: 经度、纬度，直接传nc的variable[:]就行
            data: 要画上地图的数据，理论上来说shape应该是[360, 720]或者[1, 360, 720]也行
            lat_0, lon_0: 投影纬度中心、投影经度中心
            low_lon, low_lat, up_lon, up_lat: 经度下限、纬度下限、经度上限、维度上限
            fig_title: 以防万一如果你想写标题的话
            set_cmaps: color bar
    """
    # 画图大小设置
    fig = plt.figure(figsize=(16, 9))
    plt.rc('font', size=8, weight='bold')
    ax = fig.add_subplot(111)
    if None == set_cmaps:
        set_cmaps = cmaps.NCV_jet

    # Basemap初始化，生成坐标网格，把数填进去
    m = Basemap(llcrnrlon=low_lon, llcrnrlat=low_lat, lon_0=lon_0,
                urcrnrlat=up_lat, urcrnrlon=up_lon)
    lon, lat = npy.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
    levels = m.pcolormesh(xi, yi, npy.squeeze(data), cmap=set_cmaps, latlon=True)

    # 添加格网与绘制经纬线
    m.drawparallels(npy.arange(-90., 91., 20.), labels=[1, 0, 0, 0], fontsize=8)
    m.drawmeridians(npy.arange(-180., 181., 40.), labels=[0, 0, 0, 1], fontsize=8)

    # 添加海岸线
    m.drawcoastlines()
    m.drawcountries()

    # 添加colorbar
    cbar = m.colorbar(levels, location='bottom', pad="10%")

    # 添加图的标题
    plt.title(fig_title)
    plt.show()


def csv_to_masked_array(path_to_csv, filler=1e10, crop=True, type_="ssh", choose_mask=None) -> npy.ma.masked_array:
    """把CSV文件读取为masked_array，filler表示作为fill_value的最小值，一般是不用管的

        Notice:
        ----
        注意返回值头部添加了一个维度，如数据是m×n返回值将为1×m×n
    """
    _value_array = pd.read_csv(path_to_csv).values
    if crop:
        _mask = _CROPED_MASK_SSH if type_=="ssh" else _CROPED_MASK_PREC
    else:
        _mask = _value_array>filler

    if not None is choose_mask:
        _mask = choose_mask
    
    y = npy.ma.masked_array(data=_value_array, 
                            mask=_mask, 
                            fill_value=_value_array.max())
    y = y[npy.newaxis, :, :]
    return y


class eofer:
    """ 或许我很乐意把eof部分写成工具类，不过累了明天有空再说8
    """
    pass