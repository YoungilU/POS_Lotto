# Generated by Django 4.1.1 on 2022-11-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POSApp', '0002_rename_performancedb_posdb'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posdb',
            name='balance',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='posdb',
            name='daily_sales',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='posdb',
            name='instant_lottery_1000',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='posdb',
            name='instant_lottery_2000',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='posdb',
            name='pension_lottery_1000',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='posdb',
            name='pension_lottery_5000',
            field=models.IntegerField(null=True),
        ),
    ]
