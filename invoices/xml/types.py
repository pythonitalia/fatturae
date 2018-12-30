from typing import Any, Dict, List, Union

from mypy_extensions import TypedDict


ProductSummary = TypedDict(
    "ProductSummary",
    {
        "row": int,
        "description": str,
        "quantity": str,
        "unit_price": str,
        "total_price": str,
        "vat_rate": str,
    },
)

# nested recursive types are not supported in MYPY
XMLDict = Dict[str, Union[str, int, List[Any], Any]]
