from _decimal import Decimal
from django.shortcuts import render
from rest_framework import viewsets, views
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Transaction, TradeType
from .serializers import TransactionSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class HoldingsView(views.APIView):
    """
    View to retrieve the average buy price and balance quantity for a company on a given date.
    """
    def get(self, request):
        """
        Calculates the average buy price and balance quantity.
        """
        company = request.query_params.get('company')

        if not company:
            raise ValidationError('Company are required.')

        transactions = Transaction.objects.filter(company=company).order_by('trade_date')

        holdings = []
        total_cost = 0
        total_quantity = 0

        for txn in transactions:
            if txn.trade_type == TradeType.BUY:
                holdings.append({'quantity': txn.quantity, 'price': txn.price_per_share})
                total_cost += txn.quantity * txn.price_per_share
                total_quantity += txn.quantity

            elif txn.trade_type == TradeType.SELL:
                qty_to_sell = txn.quantity
                while qty_to_sell > 0 and holdings:
                    first_lot = holdings[0]
                    if first_lot['quantity'] > qty_to_sell:
                        first_lot['quantity'] -= qty_to_sell
                        total_cost -= qty_to_sell * first_lot['price']
                        total_quantity -= qty_to_sell
                        qty_to_sell = 0
                    else:
                        qty_to_sell -= first_lot['quantity']
                        total_cost -= first_lot['quantity'] * first_lot['price']
                        total_quantity -= first_lot['quantity']
                        holdings.pop(0)

            elif txn.trade_type == TradeType.SPLIT:
                ratio = list(map(int, txn.split_ratio.split(':')))
                multiplier = ratio[1] / ratio[0]
                for lot in holdings:
                    lot['quantity'] *= int(multiplier)
                    lot['price'] /= Decimal(multiplier)
                total_quantity *= int(multiplier)

        avg_price = total_cost / total_quantity if total_quantity > 0 else 0
        return Response({
            'average_buy_price': round(avg_price, 2),
            'balance_quantity': total_quantity
        })
