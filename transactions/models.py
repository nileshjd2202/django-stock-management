from django.db import models


class TradeType(models.IntegerChoices):
    BUY = 1, "Buy"
    SELL = 2, "Sell"
    SPLIT = 3, "Split"


class Transaction(models.Model):
    trade_date = models.DateField()
    company = models.CharField(max_length=100)
    trade_type = models.PositiveSmallIntegerField(choices=TradeType.choices)
    quantity = models.PositiveIntegerField(null=True)
    price_per_share = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    split_ratio = models.CharField(max_length=10, null=True, blank=True)  # for stock splits
