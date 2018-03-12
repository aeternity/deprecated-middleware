from django.conf import settings

from aeternity.aens import NameStatus, AEName
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class AeName(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='CASCADE')
    pub_key = models.TextField(null=True)
    name = models.CharField(max_length=128)
    pointers = models.ManyToManyField(User, related_name='pointers')
    status = models.CharField(max_length=64, default=NameStatus.PRECLAIMED)

    claim_salt = models.BigIntegerField(null=True)
    name_hash = models.CharField(max_length=64, null=True)

    preclaim_tx = models.CharField(max_length=128, null=True)
    claim_tx = models.CharField(max_length=128, null=True)

    def update_from_chain(self, client):
        name = AEName(self.name, client=client)
        name.update_status()
        self.status = name.status
        self.save(update_fields=['status'])