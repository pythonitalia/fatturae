# Generated by Django 2.1.7 on 2019-02-17 12:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("invoices", "0014_item_squashed_0020_auto_20190109_1631"),
    ]

    operations = [
        migrations.AddField(
            model_name="sender",
            name="user",
            field=models.OneToOneField(
                default=1,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        )
    ]