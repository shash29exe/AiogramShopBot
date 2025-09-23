from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=200)
    telegram = models.BigIntegerField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"