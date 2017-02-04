import rtree
import fiona.crs
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

CRS = {'proj' : 'latlong', 'init': 'epsg:2263'}

def shapes_df(path):
    # index = rtree.Rtree()
    zones = gpd.read_file(path).to_crs(fiona.crs.from_epsg(2263))
    return zones.to_crs(CRS)

def people_df(path):
    f = pd.read_csv(path)
    df = pd.DataFrame(f)
    df['geometry'] = df.apply(lambda x: Point((float(x.Longitude), float(x.Latitude))), axis=1)
    df = gpd.GeoDataFrame(df, geometry='geometry')
    points = df
    points.crs = CRS
    return points

def merge(shapes, people):
    merged = gpd.sjoin(people, shapes, how = 'left', op = 'intersects')

    del merged['index_right']
    # merged.groupby('DEVELOPMEN').count().sort_values('Internal Contact ID', ascending = False).head()
    # print(merged.head())
    # zones.head()
    return merged
