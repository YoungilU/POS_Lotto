# Generated by Django 4.1.1 on 2022-11-29 22:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POSApp', '0013_remove_posdb_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='posdb',
            name='ismodify',
            field=models.BooleanField(null=True),
        ),
    ]