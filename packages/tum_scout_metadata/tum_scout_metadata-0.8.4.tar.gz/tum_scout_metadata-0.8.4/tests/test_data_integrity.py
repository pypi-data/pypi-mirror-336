import json
import os
import pydantic
import tum_scout_metadata.types as types


def test_data_integrity(directory: str) -> None:
    """Validate that the data documents correspond to the pydantic models"""
    with open(os.path.join(directory, "data", "SAMPLING.json")) as file:
        samples = pydantic.parse_obj_as(types.SampleDocument, json.load(file))
    with open(os.path.join(directory, "data", "SENSORS.json")) as file:
        sensors = pydantic.parse_obj_as(types.SensorDocument, json.load(file))
    with open(os.path.join(directory, "data", "SITES.json")) as file:
        sites = pydantic.parse_obj_as(types.SiteDocument, json.load(file))
        
    # Check that sensor and site identifiers referenced in samples exist
    for sample in samples:
        if sample.sensor_ids != "all":  # Special case
            for sensor_id in sample.sensor_ids:
                assert sensor_id in sensors, f"Sensor {sensor_id} does not exist"
        assert sample.site_id in sites, f"Site {sample.site_id} does not exist"
