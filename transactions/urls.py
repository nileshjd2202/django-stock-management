from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, HoldingsView

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('holdings/', HoldingsView.as_view(), name='holdings'),
]
