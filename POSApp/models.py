from django.db import models

# Create your models here.
class POSDB(models.Model):
    seq = models.IntegerField(primary_key=True)
    pension_lottery_1000 = models.IntegerField(null=True)
    pension_lottery_5000 = models.IntegerField(null=True)
    instant_lottery_1000 = models.IntegerField(null=True)
    instant_lottery_2000 = models.IntegerField(null=True)
    balance = models.IntegerField(null=False)
    sale = models.IntegerField(null=True)
    pay = models.IntegerField(null=True)
    sale_time = models.DateTimeField(null=True)
