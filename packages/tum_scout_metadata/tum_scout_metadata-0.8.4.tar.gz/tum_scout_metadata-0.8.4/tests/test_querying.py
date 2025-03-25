import pendulum
import tum_scout_metadata.interfaces as interfaces
import tum_scout_metadata.types as types
import pytest


def test_querying() -> None:
    sample = types.Sample(
        site_id="TEST",
        sensor_ids=[13171, 13172, 13090],
        sampling_start=pendulum.datetime(2040, 2, 1),
        sampling_end=None,
        orientation="0",
        elevation_ag="0",
        comment="This is the test sample.",
        radiation_shield= True,
    )
    
    sensor = types.Sensor(
        sensor_type="LP8",
        sensor_make="Decentlab",
        sensor_model="DL-LP8",
        start_up_date=pendulum.datetime(2022, 1, 1),
        shut_down_date=None,
        comment="This is the test sensor.",
    )
    site = types.Site(
        site_type="individual",
        site_lat=48.151,
        site_lon=11.569,
        elevation=521,
        comment="This is the test site.",
    )
    # Initialize the interface with these three test values
    interface = interfaces.Interface(
        samples=[sample],
        sensors={"13172": sensor},
        sites={"TEST": site},
    )
    # Query the interface for something valid
    metadata = interface.get(sensor_id="13172", timestamp=pendulum.datetime(2040, 2, 4))
    assert type(metadata) is types.MetaData
    # Query the interface for a sensor that doesn't exist
    with pytest.raises(AssertionError):
        interface.get(sensor_id=13173, timestamp=pendulum.datetime(2040, 2, 4))
    # Query the interface for a timestamp that doesn't have a matching sample
    with pytest.raises(AssertionError):
        interface.get(sensor_id=13172, timestamp=pendulum.datetime(2040, 1, 1))
