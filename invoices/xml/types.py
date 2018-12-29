from typing import Dict, Union, Any

# nested recursive types are not supported in MYPY
XMLDict = Dict[str, Union[str, int, Any]]
