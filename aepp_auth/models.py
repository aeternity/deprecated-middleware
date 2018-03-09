from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class AeternityUser(AbstractUser):

    email = models.EmailField(blank=True, null=True)

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)


class GithubUser(models.Model):

    user = models.ForeignKey(AeternityUser, on_delete=models.CASCADE)

    github_user_id = models.BigIntegerField(db_index=True)
    token = models.CharField(max_length=64, db_index=True)
    email = models.EmailField(blank=True, null=True)

    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)
