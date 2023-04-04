from django.db import models
from Account.models import Freelancer, User, Account
from django.utils import timezone


class Withdraw(models.Model):
    freelancer = models.ForeignKey(Freelancer, on_delete=models.DO_NOTHING)
    is_paid = models.BooleanField(default=False)
    paid_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    amount = models.BigIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    paid_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.freelancer.account.user.username


class Deposit(models.Model):
    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    authority = models.CharField(max_length=150)
    ref_id = models.CharField(max_length=100, null=True)
    is_paid = models.BooleanField(default=False)
    amount = models.BigIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    paid_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.account.user.username
