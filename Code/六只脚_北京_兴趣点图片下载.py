import pandas as pd
from bs4 import BeautifulSoup
import lxml
import requests
import geopandas as gpd
import os
import time
import random

object_path='E:\北京六只脚图片'
poi_path='E:\北京轨迹\\footprint_beijing.shp'

#写入图片信息excel#
# gdf=gpd.read_file(poi_path)
# print(gdf.columns)
# gdf.drop(['geometry'],inplace=True,axis=1)
# pd.DataFrame(gdf).to_excel(object_path+os.sep+'pic_info.xlsx')


def write_image(url,tripid,index):
    content=requests.get(url).content
    with open(object_path+os.sep+str(index)+'_'+str(int(tripid))+'.jpg','wb') as o:
        o.write(content)

df=pd.read_excel(object_path+os.sep+'pic_info_original.xlsx')
# df=df[df['pic'].notna()]
urls=list(df['pic'])


start=28867
for i in range(start,len(urls)):
    url=urls[i]
    tripid=df['tripid'][i]
    index=i
    try:
        write_image(url,tripid,index)
    except:
        print(index,tripid)
    # time.sleep(random.randint(0,2))