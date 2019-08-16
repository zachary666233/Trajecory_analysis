import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString,Point
import fiona.crs as crs
from coordTransform_utils import gcj02_to_wgs84
import os


'''读取文件路径'''
with open('E:\\全国轨迹\\path.txt','r',encoding='utf-8')as o:
    paths=o.read().strip().split('\n')
poi_paths=[path for path in paths if 'footprints' in path]
line_paths=[path for path in paths if 'track' in path]


def line_clean(coords):
    '''输入((x1,y1),(x2,y2))形式的数据,输出标记
    1：删除该线段
    0：保留该线段'''
    for xy in coords:
        if xy[0]>180 or xy[0]<-180 or xy[1]>90 or xy[1]<-90:
            return 1
    return 0

def point_clean(coords):
    '''输入((x,y)形式的数据,输出标记
    1：删除该线段
    0：保留该线段'''
    for xy in coords:
        if xy[0][0]>180 or xy[0][0]<-180 or xy[0][1]>90 or xy[0][1]<-90:
            return 1
        return 0

'''轨迹数据'''
#保存名称为footprint#
i = 1
for path in line_paths[i-1:]:
    try:
        gdf = gpd.GeoDataFrame.from_file(path)
        gdf['xy'] = gdf['geometry'].apply(lambda x: x.coords)
        gdf['judge'] = gdf['xy'].apply(line_clean)
        gdf = gdf[gdf['judge'] == 0]

        gdf.drop(['judge'], inplace=True, axis=1)

        gdf['geometry'] = gdf['xy'].apply(lambda x: LineString([gcj02_to_wgs84(x[0],x[1]) for x in x]))
        gdf.drop(['xy'], inplace=True, axis=1)

        gpd.GeoDataFrame(gdf).to_file('E:\\全国轨迹清洗\\footprint(' + str(i) + ').shp')  # 输出的文件为84坐标系
    except:
        print(i,path)
    finally:
        i+=1