from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class GithubUser(AbstractUser):

    user_id = models.BigIntegerField(db_index=True)
    token = models.CharField(max_length=64, db_index=True)
    email = models.EmailField(blank=True, null=True)

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
