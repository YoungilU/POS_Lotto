# Generated by Django 4.1.1 on 2022-11-18 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POSApp', '0007_remove_posdb_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='posdb',
            name='sale_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='posdb',
            name='balance',
            field=models.IntegerField(),
        ),
    ]