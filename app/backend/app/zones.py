import pandas as pd
import geopandas as gpd
from haversine import haversine, Unit

zones = gpd.read_file("contents/taxi_zones.shp")
zones_m = zones.to_crs(epsg=3857)

zones_m["centroid"] = zones_m.geometry.centroid.to_crs(epsg=4326)
zones_m = zones_m.set_geometry("centroid").to_crs(epsg=4326)

zones_m["lat"] = zones_m.centroid.y
zones_m["lon"] = zones_m.centroid.x

coords = {
    int(row["LocationID"]): (row["lat"], row["lon"])
    for _, row in zones_m.iterrows()
}

def calculate_trip_distance(from_id, to_id):
    return haversine(
        coords[int(from_id)],
        coords[int(to_id)],
        unit=Unit.MILES
    )

def get_zones():
    path = "contents/taxi_zone_lookup.csv"
    data = pd.read_csv(path)
    data = data.drop(columns=["Borough", "service_zone"])

    result = {}

    for _, row in data.iterrows():
        result[str(row["LocationID"])] = row["Zone"]

    return result
