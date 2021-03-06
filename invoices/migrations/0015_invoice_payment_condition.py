# Generated by Django 2.1.5 on 2019-02-10 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("invoices", "0014_item_squashed_0020_auto_20190109_1631")]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="payment_condition",
            field=models.CharField(
                choices=[
                    ("TP01", "pagamento a rate"),
                    ("TP02", "pagamento completo"),
                    ("TP03", "anticipo"),
                ],
                default="TP01",
                max_length=5,
                verbose_name="Payment condition",
            ),
            preserve_default=False,
        )
    ]
