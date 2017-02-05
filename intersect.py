import fiona.crs
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

CRS = {
    'proj': 'latlong',
    'init': 'epsg:2263'
}


def shapes_df(path):
    zones = gpd.read_file(path).to_crs(fiona.crs.from_epsg(2263))
    return zones.to_crs(CRS)


def to_point(person):
    lat = float(person.Longitude)
    lng = float(person.Latitude)
    return Point((lat, lng))


def people_df(path):
    f = pd.read_csv(path)
    df = pd.DataFrame(f)
    df['geometry'] = df.apply(lambda x: to_point(x), axis=1)
    df = gpd.GeoDataFrame(df, geometry='geometry')
    points = df
    points.crs = CRS
    return points


def merge(shapes, people):
    merged = gpd.sjoin(people, shapes, how='left', op='intersects')
    del merged['index_right']
    return merged
