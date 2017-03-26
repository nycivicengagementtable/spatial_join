import fiona.crs
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from shapely.geometry.multipolygon import MultiPolygon
import re
import pdb


EPSG = 2263

CRS = {
    'proj': 'latlong',
    'init': 'epsg:{:d}'.format(EPSG)
}

LAT_REGEX = re.compile('\\blat(itude)?\\b', flags=re.I)
LNG_REGEX = re.compile('\\blo?ng(itude)?\\b', flags=re.I)

# handle geo/json shape files

def explode_shape_data(path):
    """Break down multipolygons in geojson to single polygons per row.
    Code from here: https://gist.github.com/mhweber/cf36bb4e09df9deee5eb54dc6be74d26"""
    indf = gpd.GeoDataFrame.from_file(path)
    outdf = gpd.GeoDataFrame(columns=indf.columns)
    for idx, row in indf.iterrows():
        if type(row.geometry) == Polygon:
            outdf = outdf.append(row,ignore_index=True)
        if type(row.geometry) == MultiPolygon:
            multdf = gpd.GeoDataFrame(columns=indf.columns)
            recs = len(row.geometry)
            multdf = multdf.append([row]*recs,ignore_index=True)
            for geom in range(recs):
                multdf.loc[geom,'geometry'] = row.geometry[geom]
            outdf = outdf.append(multdf,ignore_index=True)
    return outdf

def shapes_df(path):
    """Convert raw geojson data to geopandas dataframe with correct coordinates per CRS/EPSG"""
    raw_shapes = explode_shape_data(path)
    raw_shapes.crs = fiona.crs.from_epsg(EPSG) # set the crs on the dataframe to prevent "naive geometry" error
    return raw_shapes.to_crs(CRS)


# process people csv data

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
    """Convert raw people (voter) data to geopandas dataframe according to EPSG/CRS"""
    raw_people = pd.read_csv(path)
    raw_people['geometry'] = raw_people.apply(lambda x: to_point(x), axis=1)
    points = gpd.GeoDataFrame(raw_people, geometry='geometry')
    points.crs = CRS
    return points


# merge people and shape files

def merge_within(shapes, people):
    """Merge people csv geodataframe and shapes geodataframe, retaining all people data despite match rate."""
    # Per http://geopandas.org/mergingdata.html, "within", "intersects", and "contains" are the same, but only "within" and "intersects" results in the same number of rows upon merge, and "within" was most consistent.
    merged = gpd.sjoin(people, shapes, how='left', op='within')
    del merged['geometry']
    del merged['index_right']
    return merged
