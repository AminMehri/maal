from django.db import models
from Account.models import Account, User, Freelancer
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField
import json
from pathlib import Path


# تا پابیلیش نشده فرصت کنسل داره
class Project(models.Model):
    
    with open(Path(__file__).resolve().parent / 'categories.json', "r") as file:
        data = json.load(file)["categories"]
        CATEGORY_CHOICES = *((x,x) for x in data),
    
    owner = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    admin_confirmed = models.BooleanField(default=False)
    confirmed_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=250)
    total_price = models.BigIntegerField()
    price = models.BigIntegerField()
    fee_percent = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.CharField(max_length=5000)
    categories = ArrayField(models.CharField(choices=CATEGORY_CHOICES, max_length=100))
    is_full = models.BooleanField(default=False)
    files = ArrayField(models.FileField(upload_to="projects/files"))       # تا پابلیش نشده فایلارو نمیده
    publish = models.BooleanField(default=False)    # نوتیف میده که استوریتو بزار یه ساعت وقت داری, 
    published_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)


class AcceptedProject(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    freelancer = models.ForeignKey(Freelancer, on_delete=models.DO_NOTHING)
    pending = models.BooleanField(default=False)
    request_at = models.DateTimeField(default=timezone.now)
    accept_at = models.DateTimeField()
    price = models.BigIntegerField()
    followers = models.IntegerField()  # این سه مورد برای اینه که داشته باشیم فریلنسر در زمان پذیرش یک کار وضعیت پیجش به چه صورت بوده, چون هی این مقادیر از فیلد اصلی اکانت عوض میشه
    following = models.IntegerField()
    engagement = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])

    
    def check_end_time(self, obj):
        pass

