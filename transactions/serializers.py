from rest_framework import serializers
from .models import Transaction, TradeType


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate_transaction_type(self, value):
        """
        Validates the transaction type.
        """
        if value not in TradeType.values:
            raise serializers.ValidationError("Invalid transaction type. Must be BUY, SELL, or SPLIT.")
        return value

    def validate(self, attrs):
        """
        Validates the transaction data, for SELL transactions.
        Ensures that the quantity being sold is not greater than the current holdings.
        """
        transaction_type = attrs.get('transaction_type')
        quantity = attrs.get('quantity')
        company = attrs.get('company')
        date = attrs.get('date')  # Added date to filter

        if transaction_type == TradeType.SELL:
            # Calculate current holdings for the company before applying the new transaction
            current_holdings = Transaction.objects.filter(company=company, date__lte=date).aggregate(
                total_buy=Sum('quantity', filter=models.Q(transaction_type=TradeType.BUY)),
                total_sell=Sum('quantity', filter=models.Q(transaction_type=TradeType.SELL))
            )
            total_buy = current_holdings['total_buy'] or 0
            total_sell = current_holdings['total_sell'] or 0
            available_quantity = total_buy - total_sell

            if quantity > available_quantity:
                raise ValidationError(
                    f"Not enough shares to sell. Available: {available_quantity}, Requested: {quantity}")

        if transaction_type == TradeType.SPLIT:
            split_ratio = attrs.get('split_ratio')
            ratio_list = split_ratio.split(':')
            if len(ratio_list) != 2:
                raise ValidationError('Invalid split ratio format. Please use the format "X:Y", e.g., "1:2".')

        return attrs
