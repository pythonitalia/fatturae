# Generated by Django 2.1.4 on 2018-12-30 15:36

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import invoices.utils


class Migration(migrations.Migration):

    dependencies = [("invoices", "0008_auto_20181229_2240")]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="invoice_summary",
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default=[],
                validators=[
                    invoices.utils.JSONSchemaValidator(
                        {
                            "$schema": "http://json-schema.org/draft-04/schema#",
                            "items": [
                                {
                                    "properties": {
                                        "description": {"type": "string"},
                                        "quantity": {"type": "string"},
                                        "row": {"type": "integer"},
                                        "total_price": {"type": "string"},
                                        "unit_price": {"type": "string"},
                                        "vat_rate": {"type": "string"},
                                    },
                                    "required": [
                                        "row",
                                        "description",
                                        "quantity",
                                        "unit_price",
                                        "total_price",
                                        "vat_rate",
                                    ],
                                    "type": "object",
                                }
                            ],
                            "type": "array",
                        }
                    )
                ],
            ),
            preserve_default=False,
        )
    ]