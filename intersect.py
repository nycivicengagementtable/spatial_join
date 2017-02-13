import fiona.crs
import geopandas as gpd
import pandas as pd
import re
from shapely.geometry import Point
import pdb

EPSG = 2263

CRS = {
    'proj': 'latlong',
    'init': 'epsg:{:d}'.format(EPSG)
}

LAT_REGEX = re.compile('\\blat(itude)?\\b', flags=re.I)
LNG_REGEX = re.compile('\\blo?ng(itude)?\\b', flags=re.I)


def shapes_df(path):
    zones = gpd.read_file(path).to_crs(fiona.crs.from_epsg(EPSG))
    return zones.to_crs(CRS)


def find_key(keys, regex):
    results = filter(regex.match, keys)
    results_iter = (result for result in results)
    return next(results_iter, None)


def to_point(person):
    keys = person.keys()
    lat_key = find_key(keys, LAT_REGEX)
    lng_key = find_key(keys, LNG_REGEX)

    lat = float(person[lat_key])
    lng = float(person[lng_key])
    return Point((lng, lat))


def people_df(path):
    f = pd.read_csv(path)
    df = pd.DataFrame(f)
    df['geometry'] = df.apply(lambda x: to_point(x), axis=1)
    df = gpd.GeoDataFrame(df, geometry='geometry')
    points = df
    points.crs = CRS
    return points


def merge(shapes, people):
    pdb.set_trace()
    merged = gpd.sjoin(people, shapes, how='left', op='intersects')
    del merged['geometry']
    del merged['index_right']
    return merged
