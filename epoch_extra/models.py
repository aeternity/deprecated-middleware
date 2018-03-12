from django.conf import settings

from aeternity.aens import NameStatus, AEName
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

from epoch_extra import get_client, get_key_pair

User = get_user_model()


class AeName(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete='CASCADE')
    pub_key = models.TextField(null=True)
    name = models.CharField(max_length=128)
    pointers = models.ManyToManyField(User, related_name='pointers')
    status = models.CharField(max_length=64, default=NameStatus.PRECLAIMED)

    claim_salt = models.CharField(max_length=64, null=True)
    name_hash = models.CharField(max_length=64, null=True)

    preclaim_tx = models.CharField(max_length=128, null=True)
    claim_tx = models.CharField(max_length=128, null=True)

    def update_from_chain(self):
        client = get_client()
        name = AEName(self.name, client=client)
        name.update_status()
        self.status = name.status
        self.save(update_fields=['status'])

    def preclaim(self):
        client = get_client()
        name = AEName(self.name, client=client)
        key_pair = get_key_pair()
        tx_hash, salt = name.preclaim(key_pair)
        self.preclaim_tx = tx_hash
        self.claim_salt = salt
        self.save(update_fields=['claim_salt', 'preclaim_tx'])

    def claim(self):
        client = get_client()
        name = AEName(self.name, client=client)
        name.preclaim_salt = int(self.claim_salt)
        key_pair = get_key_pair()
        tx_hash, _ = name.claim(key_pair)
        self.claim_tx = tx_hash
        self.save(update_fields=['claim_tx'])
