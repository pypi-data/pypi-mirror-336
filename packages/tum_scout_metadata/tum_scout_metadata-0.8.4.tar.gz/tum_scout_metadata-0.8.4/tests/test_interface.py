
import pendulum

from dotenv import dotenv_values
from tum_scout_metadata import interfaces


def test_interface() ->None: 
    """Test access to the github interface and check if data can be downloaded.
    """
  
    interface = interfaces.load_from_github(
        github_repository=dotenv_values(".env")["GITHUB_URL"],
        access_token=dotenv_values(".env")["GITHUB_KEY"],
    )
    metadata = interface.get(sensor_id = '13094', timestamp=pendulum.datetime(2022, 11, 21))
    assert metadata.site_id =='CLIM'
    