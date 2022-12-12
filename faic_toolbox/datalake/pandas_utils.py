import pandas as pd
import requests
from typing import Optional
import io


def dataframe_from_datalake(
    layer: str,
    source_type: str,
    source_name: str,
    ts: str,
    table: str,
    custom_headers: Optional[dict] = {},
) -> pd.DataFrame:
    """Retreive a dataframe from datalake

    Args:
        layer (str): datalake layer
        source_type (str): source type (web, facebook, etc.)
        source_name (str): source name (active-users, sensordata, etc.)
        ts (str): timestamp (use 'global' if not needed)
        table (str): table name
        custom_headers (Optional[dict], optional): custom headers. Defaults to {}.

    Returns:
        pd.DataFrame: The retreived dataframe
    """
    from .config import datalake

    assert datalake is not None, "no datalake config found"
    # Get a presigned url from s3
    get_url_endpoint = (
        f"{datalake.base_url}/{layer}/{source_type}/{source_name}/{ts}/{table}"
    )
    url = requests.get(
        get_url_endpoint,
        headers={**datalake.get_headers, **custom_headers},
    ).json()["url"]
    file_content = requests.get(url).content.decode()
    file_string = io.StringIO(file_content)
    return pd.read_csv(file_string)


def save_dataframe(
    df: pd.DataFrame,
    layer: str,
    source_type: str,
    source_name: str,
    ts: str,
    table: str,
    custom_headers: Optional[dict] = {},
) -> requests.models.Response:
    """Save a dataframe to datalake

    Args:
        df (pd.DataFrame): the dataframe
       layer (str): datalake layer
        source_type (str): source type (web, facebook, etc.)
        source_name (str): source name (active-users, sensordata, etc.)
        ts (str): timestamp (use 'global' if not needed)
        table (str): table name
        custom_headers (Optional[dict], optional): custom headers. Defaults to {}.

    Returns:
        requests.models.Response: Request response
    """
    from .config import datalake

    assert datalake is not None, "no datalake config found"
    put_url_endpoint = (
        f"{datalake.base_url}/{layer}/{source_type}/{source_name}/{ts}/{table}"
    )
    url = requests.put(
        url=put_url_endpoint,
        headers={**datalake.get_headers, **custom_headers},
    ).json()["url"]

    csv = df.to_csv(index=False)

    return requests.put(url=url, data=csv, headers={"Content-Type": "text/csv"})
