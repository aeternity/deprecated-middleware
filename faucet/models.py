from __future__ import unicode_literals

from datetime import timedelta

from django.db import models

# Create your models here.
from django.db.models import Count, Sum
from django.utils import timezone


class FaucetTransaction(models.Model):

    TOKEN_PER_DAY_MAXIMUM = 200

    public_key = models.CharField(max_length=128, primary_key=True)
    amount = models.FloatField()
    transfered_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def receivable_tokens(cls, public_key):
        now = timezone.now()
        today = now.date()
        tomorrow = today + timedelta(days=1)
        todays_transactions = cls.objects.filter(
            public_key=public_key,
            transfered_at__lt=tomorrow,
            transfered_at__gte=today
        )

        amount = 0
        if todays_transactions:
            amount = (
                todays_transactions
                .values_list('public_key')
                .annotate(todays_amount=Sum('amount'))
            )

        # print(list(amount))
        # [0]['todays_amount']
        # amount = 1
        return max(0, cls.TOKEN_PER_DAY_MAXIMUM - amount)
