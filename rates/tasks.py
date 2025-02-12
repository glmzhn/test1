from celery import shared_task
import requests
from django.core.cache import cache
from .models import ExchangeRate


@shared_task
def fetch_exchange_rate():
    url = "https://api.frankfurter.dev/v1/latest"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        rates = data.get("rates", {})

        currency = "USD"
        rate = rates.get(currency)

        if rate:
            ExchangeRate.objects.update_or_create(
                currency=currency,
                defaults={"rate": rate}
            )
            cache.set(f"exchange_rate_{currency}", rate, timeout=60)

            return f"Updated {currency}: {rate}"
    return "Failed to fetch exchange rate"
