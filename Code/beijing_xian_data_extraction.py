import geopandas as gpd
import pandas as pd
from shapely.geometry import LineString,Point
import fiona.crs as crs
from fiona.crs import from_epsg
from coordTransform_utils import gcj02_to_wgs84
import os
import matplotlib.pyplot as plt

xian_base=gpd.GeoDataFrame.from_file('D:\中规院信息中心智慧城市\西安六只脚分析\大西安区县shp\\大西安区县.shp',encoding='utf-8')
xian_base=xian_base.dissolve(by='Province')

beijing_base=gpd.GeoDataFrame.from_file('D:\中规院信息中心智慧城市\北京乡村DOU研究\乡村矢量数据\\北京市域边界_84.shp')
print(beijing_base.crs)

line_paths=['E:\全国轨迹预处理\\'+x for x in os.listdir('E:\全国轨迹预处理') if 'track' in x and 'shp' in x]
poi_paths=['E:\全国轨迹预处理\\'+x for x in os.listdir('E:\全国轨迹预处理') if 'footprint.shp' and 'shp' in x]


where='xian'    #'beijing'
frame=[]
i = 1
for path in line_paths[i-1:]:
        gdf = gpd.GeoDataFrame.from_file(path)
        gdf.crs={'init': 'epsg:4326'}
        # gdf=gdf.to_crs({'init': 'epsg:3857'})
        gdf['judge'] = gdf['geometry'].apply(lambda x:beijing_base.contains(Point(x.coords[0])).bool() and
                                                    beijing_base.contains(Point(x.coords[-1])).bool())
        gdf = gdf[gdf['judge'] == True]

        gdf.drop(['judge'], inplace=True, axis=1)
        frame.append(gdf)

gpd.GeoDataFrame(pd.concat(frame)).to_file('E:\北京轨迹\\track_beijing.shp')  # 输出的文件为84投影
