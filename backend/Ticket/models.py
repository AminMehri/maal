from django.db import models
from Account.models import Account
from django.utils import timezone
from Admin.models import Admin


class Conversation(models.Model):

    STATUS_CHOICES = (
        ('Answered', 'Answered'),
        ('Pending', 'Pending'),
        ('Closed', 'Closed')
    )

    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=256)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField()    # Sort by last_update in Tickets List

    def __str__(self):
        return self.subject



class Ticket(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=2048)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.conversation.subject
    


class AdminAnswer(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.DO_NOTHING)
    admin = models.ForeignKey(Admin, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=4096)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.conversation.subject