from django.db import models
from Account.models import Account
from django.utils import timezone
from Admin.models import Admin



class Ticket(models.Model):
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=256)
    description = models.CharField(max_length=1028)
    is_awnsered = models.BooleanField(default=False)
    responsive_admin = models.ForeignKey(Admin, on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.subject
