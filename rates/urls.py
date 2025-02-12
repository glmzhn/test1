from django.urls import path
from .views import ExchangeRateView

urlpatterns = [
    path("rate/", ExchangeRateView.as_view(), name="exchange_rate"),
]
