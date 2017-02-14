import rtree # this is currently not used, do we keep it?
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
    #df = pd.read_csv(path) # maybe just this? get a dataframe from a file
    f = pd.read_csv(path)
    df = pd.DataFrame(f) # isn't this is redundant

    def point(x):
        return Point((float(x.Longitude), float(x.Latitude)))

    df['geometry'] = df.apply(point, axis=1)
    points = gpd.GeoDataFrame(df, geometry='geometry')
    points.crs = CRS
    return points

def merge(shapes, people):
    """Do a spatial join on people and shapes, return new dataframe"""
    merged = gpd.sjoin(people, shapes, how = 'left', op = 'intersects')

    del merged['index_right'] # what is this? probably index from the shapes? probably don't need?
    # merged.groupby('DEVELOPMEN').count().sort_values('Internal Contact ID', ascending = False).head()
    # print(merged.head())
    # zones.head()
    return merged


import unittest

class Tests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.shape_path = "shape_file"   # TODO get some test files, or update
        cls.people_path = "people_file" # signatures to take stringio objects

    def test_shapes_df(self):
        self.assertIsInstance(shapes_df(self.shape_path), pd.DataFrame)

    def test_people_df(self):
        self.assertIsInstance(people_df(self.people_path), pd.DataFrame)

    def test_merge(self):
        shapes = shapes_df(self.shapes_path)
        people = people_df(self.people_path)
        self.assertIsInstance(merge(shapes, people), pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
