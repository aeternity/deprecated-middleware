from __future__ import unicode_literals

from datetime import timedelta

from django.db import models

# Create your models here.
from django.db.models import Sum
from django.utils import timezone
from constance import config


class FaucetTransaction(models.Model):

    public_key = models.CharField(max_length=128, db_index=True)
    amount = models.DecimalField()
    transferred_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def _get_spent_aggregate(qs):
        consumed_aggregate = qs.values('public_key').annotate(spent=Sum('amount'))
        return consumed_aggregate[0]['spent'] if consumed_aggregate else 0

    @classmethod
    def receivable_tokens(cls, public_key):
        now = timezone.now()
        today = now.date()
        earlier = now.date() - timedelta(hours=1)
        tomorrow = today + timedelta(days=1)

        hourly_limit = config.FAUCET_HOURLY_LIMIT
        daily_limit = config.FAUCET_DAILY_LIMIT

        txs_today = cls.objects.filter(
            public_key=public_key,
            transfered_at__lt=tomorrow,
            transfered_at__gte=today
        )

        txs_last_hour = txs_today.filter(
            transfered_at__lt=now,
            transfered_at__gte=earlier
        )

        consumed_last_hour = cls._get_spent_aggregate(txs_last_hour)
        hourly_available = max(0, hourly_limit - consumed_last_hour)

        if hourly_available == 0:
            return 0

        consumed_last_day = cls._get_spent_aggregate(txs_today)
        daily_available = max(0, daily_limit - consumed_last_day)

        return min(daily_available, hourly_available)
