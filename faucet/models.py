from __future__ import unicode_literals

from datetime import timedelta

from django.db import models

# Create your models here.
from django.db.models import Sum
from django.utils import timezone
from constance import config


class FaucetTransaction(models.Model):

    public_key = models.CharField(max_length=128, db_index=True)
    amount = models.FloatField()
    transfered_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def receivable_tokens(cls, public_key):
        now = timezone.now()
        today = now.date()
        earlier = now.date() - timedelta(hours=1)
        tomorrow = today + timedelta(days=1)

        hourly_limit = config.FAUCET_HOURLY_LIMIT
        daily_limit = config.FAUCET_DAILY_LIMIT

        todays_transactions = cls.objects.filter(
            public_key=public_key,
            transfered_at__lt=tomorrow,
            transfered_at__gte=today
        )

        txs_last_hour = todays_transactions.filter(
            transfered_at__lt=now,
            transfered_at__gte=earlier
        )
        consumed_last_hour = txs_last_hour.values('public_key').annotate(spent=Sum('amount'))

        consumed = 0
        if consumed_last_hour:
            consumed = consumed_last_hour[0]['spent']

        hourly_available = max(0, hourly_limit - consumed)

        if hourly_available == 0:
            return 0

        consumed_last_day = todays_transactions.values('public_key').annotate(spent=Sum('amount'))
        consumed = 0
        if consumed_last_day:
            consumed = consumed_last_day[0]['spent']

        daily_available = max(0, daily_limit - consumed)

        return min(daily_available, hourly_available)
