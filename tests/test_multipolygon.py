import pytest

from postgis import MultiPolygon, Polygon

MULTI = (
            (
                ((35, 10), (45, 45), (15, 40), (10, 20), (35, 10)),
                ((20, 30), (35, 35), (30, 20), (20, 30))
            ),
            (
                ((36, 10), (46, 45), (16, 40), (16, 20), (36, 10)),
                ((21, 30), (36, 35), (36, 20), (21, 30))
            ),
        )


@pytest.mark.parametrize('expected', [
    MULTI,
])
def test_multipolygon_should_round(cursor, expected):
    params = [MultiPolygon(expected, srid=4326)]
    cursor.execute('INSERT INTO multipolygon (geom) VALUES (%s)', params)
    cursor.execute('SELECT geom FROM multipolygon WHERE geom=%s', params)
    geom = cursor.fetchone()[0]
    assert geom.coords == expected


def test_multilinestring_geojson():
    multi = MultiPolygon(MULTI)
    assert multi.geojson == {
        "type": "MultiPolygon",
        "coordinates": MULTI
    }


def test_geom_should_compare_with_coords():
    assert MULTI == MultiPolygon(MULTI)


def test_multipolygon_get_item():
    multi = MultiPolygon(MULTI)
    assert multi[0] == Polygon(MULTI[0])
