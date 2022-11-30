from django.db import models

# Create your models here.
class POSDB(models.Model):
    seq = models.IntegerField(primary_key=True)
    pension_lottery_1000 = models.IntegerField(null=True)
    pension_lottery_5000 = models.IntegerField(null=True)
    instant_lottery_1000 = models.IntegerField(null=True)
    instant_lottery_2000 = models.IntegerField(null=True)
    pension_lottery_1000_Qty = models.IntegerField(null=True)
    pension_lottery_5000_Qty = models.IntegerField(null=True)
    instant_lottery_1000_Qty = models.IntegerField(null=True)
    instant_lottery_2000_Qty = models.IntegerField(null=True)
    sale = models.IntegerField(null=True)
    pay = models.IntegerField(null=True)
    sale_time = models.DateTimeField(null=True)
    daily_sale_start = models.DateTimeField(null=True)
    base_balance = models.IntegerField(null=True)
    ismodify = models.BooleanField(null=True)
