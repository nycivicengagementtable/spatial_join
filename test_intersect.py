from intersect import *
import pandas as pd
import pytest
from pytest import approx


@pytest.mark.parametrize('headings', [
    (['ID', 'Latitude', 'Longitude']),
])
def test_to_point(headings):
    # the numbers are arbitrary
    person_id = 5
    lat = 40.687482
    lng = -73.963384

    person = pd.Series([person_id, str(lat), str(lng)], index=headings)
    point = to_point(person)

    assert point.x == approx(lng)
    assert point.y == approx(lat)
