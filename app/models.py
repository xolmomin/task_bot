from django.db import models
from django.utils import timezone


class TgUser(models.Model):
    user_id = models.IntegerField()
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.user_id}'


class History(models.Model):
    tg_user = models.ForeignKey(TgUser, on_delete=models.CASCADE, related_name='user_history')
    text = models.CharField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.tg_user_id}'
