import datetime

from django.db import models

import requests

import json

# Create your models here.

class StockRank(models.Model):
    rank_num = models.IntegerField(null=False)
    symbol_code = models.CharField(max_length=200)
    corp_name = models.CharField(max_length=200)
    def __str__(self):
        return self.corp_name

class DailyStock(models.Model):
    symbol_code = models.ForeignKey('StockRank.symbol_code', on_delete=models.CASCADE)
    date = models.DateTimeField('update date')
    trade_price = models.IntegerField(default=0)
    trade_time = models.TimeField('trade time')
    def __str__(self):
        return self.trade_price
