from django.db import models
from Account.models import Account

# admin rules TODO:
class Admin(models.Model):
    ADMIN_RULE = (
        ("superuser", "superuser"),
        ("admin", "admin"),
        ("unknown", "unknown"),
    )
    user = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, blank=True)
    admin_rule = models.CharField(choices=ADMIN_RULE, max_length=15)

    def __str__(self):
        return self.user.user.username