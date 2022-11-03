from typing import Union
from dataclasses import dataclass, field
import os


@dataclass
class DatalakeConfig:

    base_url: str
    api_key: str = os.getenv("DATALAKE_KEY", "null")

    def __post_init__(self):
        self.get_headers = {"x-api-key": self.api_key}


datalake: Union[DatalakeConfig, None] = None
