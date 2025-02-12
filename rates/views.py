from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer


class ExchangeRateView(APIView):
    def get(self, request, currency="USD"):
        cached_rate = cache.get(f"exchange_rate_{currency}")

        if cached_rate is not None:
            return Response({"currency": currency, "rate": cached_rate})

        try:
            rate = ExchangeRate.objects.get(currency=currency)
            serializer = ExchangeRateSerializer(rate)
            return Response(serializer.data)
        except ExchangeRate.DoesNotExist:
            return Response({"error": "Rate not found"}, status=404)
