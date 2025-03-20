from django.db.models import Sum,Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Transaction, TradeType


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate(self, attrs):
        """
        Validates the transaction data, for SELL transactions.
        Ensures that the quantity being sold is not greater than the current holdings.
        """
        trade_type = attrs.get('trade_type')
        quantity = attrs.get('quantity')
        company = attrs.get('company')
        trade_date = attrs.get('trade_date')  # Added date to filter

        if trade_type == TradeType.SELL:
            # Calculate current holdings for the company before applying the new transaction
            current_holdings = Transaction.objects.filter(company=company, trade_date__lte=trade_date).aggregate(
                total_buy=Sum('quantity', filter=Q(trade_type=TradeType.BUY)),
                total_sell=Sum('quantity', filter=Q(trade_type=TradeType.SELL))
            )
            total_buy = current_holdings['total_buy'] or 0
            total_sell = current_holdings['total_sell'] or 0
            available_quantity = total_buy - total_sell

            if quantity > available_quantity:
                raise ValidationError({
                    "quantity": f"Not enough shares to sell. Available: {available_quantity}, Requested: {quantity}"
                })

        if trade_type == TradeType.SPLIT:
            split_ratio = attrs.get('split_ratio')
            ratio_list = split_ratio.split(':')
            if len(ratio_list) != 2:
                raise ValidationError({
                    "split ratio": "Invalid split ratio format. Please use the format 'X:Y', e.g., '1:2'."
                })

        return attrs
