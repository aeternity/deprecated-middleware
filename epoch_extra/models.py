from aeternity.aens import NameStatus
from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class AeName(models.Model):

    user = models.ForeignKey(User, on_delete='CASCADE')
    pub_key = models.TextField(null=True)
    name = models.CharField(max_length=128)
    pointers = models.ManyToManyField(User, related_name='pointers')
    status = models.CharField(max_length=64, default=NameStatus.PRECLAIMED)