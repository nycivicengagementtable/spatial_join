from intersect import *
import pandas as pd
import pytest
from pytest import approx
import random


@pytest.mark.parametrize('headings', [
    (['ID', 'Latitude', 'Longitude']),
    (['ID', 'Latitude ', 'longitude']),
    (['ID', 'lat', 'lng']),
])

def test_to_point(headings):
    # the numbers are arbitrary
    person_id = random.randint(1, 10)
    # http://www.spatialreference.org/ref/epsg/nad83-new-york-long-island-ftus/
    lat = random.uniform(41.3100, 40.4700)
    lng = random.uniform(-74.2700, -71.7500)

    person = pd.Series([person_id, str(lat), str(lng)], index=headings)
    point = to_point(person)

    assert point.x == approx(lng)
    assert point.y == approx(lat)


@pytest.mark.parametrize('people_path, num_nulls', [
    ('sample_data/people/cvh_people_small.csv', 0),
    ('sample_data/people/cvh_people_with_missing.csv', 1),
])

def test_merge(people_path, num_nulls):
    people = people_df(people_path)
    shapes = shapes_df('sample_data/shapes/nycha.json')
    merged = merge_within(shapes, people)

    assert len(merged["Internal Contact ID"]) == len(merged["BoroCD"])
    assert len(merged[merged["BoroCD"].isnull()]) == num_nulls
