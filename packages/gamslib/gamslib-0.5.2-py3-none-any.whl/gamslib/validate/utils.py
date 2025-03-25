import functools
import os
from pathlib import Path
import requests
import uritools



@functools.lru_cache
def load_schema(schema_file: str) -> bytes:
    """Load a schema file from file or URL and return its content as bytes."""
    schema_data = None
    if os.path.isfile(schema_file):
        return Path(schema_file).read_bytes()
    
    parts = uritools.urisplit(schema_file)
    if parts.isuri():
        if parts.scheme == "file":
            try:
                schema_data = Path(parts.path).read_bytes()
            except FileNotFoundError as exp:
                raise ValueError(f"Cannot open schema file '{schema_file}': Wrong path or URL?") from exp
        elif parts.scheme in ('http', 'https'):
            response = requests.get(schema_file)
            try:
                response.raise_for_status()
                schema_data = response.content
            except requests.exceptions.HTTPError as exp:
                raise ValueError(f"Cannot open schema file '{schema_file}': {response.reason}") from exp
        else:
            raise ValueError(f"I do not know how to open '{schema_file}'")
    else:
        raise ValueError(f"Cannot open schema file '{schema_file}': Wrong path or URL?")
    return schema_data
