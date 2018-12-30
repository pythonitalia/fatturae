from django.utils.deconstruct import deconstructible

from jsonschema import validate


PRODUCT_SUMMARY_SCHEMA = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "type": "array",
    "items": [
        {
            "type": "object",
            "properties": {
                "row": {"type": "integer"},
                "description": {"type": "string"},
                "quantity": {"type": "number"},
                "unit_price": {"type": "number"},
                "total_price": {"type": "number"},
                "vat_rate": {"type": "number"},
            },
            "required": [
                "row",
                "description",
                "quantity",
                "unit_price",
                "total_price",
                "vat_rate",
            ],
        }
    ],
}


@deconstructible
class JSONSchemaValidator:
    def __init__(self, schema):
        self.schema = schema

    def __call__(self, value):
        validate(value, self.schema)

    def __eq__(self, other):
        return self.schema == other.schema
