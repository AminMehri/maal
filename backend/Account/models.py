from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import ArrayField



class User(AbstractUser):
    pass


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email_verify_token = models.CharField(max_length=256, null=True)
    email_verify_generate_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    email_verified = models.BooleanField(default=False)
    reset_token_created_at = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    reset_password_token = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    balance = models.BigIntegerField(default=0)

    def __str__(self):
        return self.user.username


class InstagramAccount(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    instagram_id = models.CharField(max_length=256)
    is_verify = models.BooleanField(default=False)
    instagram_otp = models.IntegerField()
    followers = models.IntegerField(null=True)
    following = models.IntegerField(null=True)
    engagement = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    hashtags = ArrayField(models.CharField(max_length=100))
    uploads = models.IntegerField(null=True)
    post_per_day = models.FloatField(null=True)
    profile = models.FileField(upload_to="profiles")
    full_name = models.CharField(max_length=1000, null=True)
    bio = models.CharField(max_length=2500, null=True)
    category = models.CharField(max_length=250, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_delete = models.BooleanField(default=False)
    delete_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.account.user.username

    def update(self, obj):
        pass


class Freelancer(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    instagram_account = models.ForeignKey(InstagramAccount, on_delete=models.DO_NOTHING)
    is_accepted = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    verified_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    reject_reason = models.CharField(max_length=2500, null=True, blank=True)

    def __str__(self):
        return self.account.user.username



class Rule(models.Model):

    RULES_CHOICES = (
        ("newUser", "newUser"),
        ("Ban", "Ban"),
        ("bronzeDiscount", "bronzeDiscount"),
        ("silverDiscount", "silverDiscount"),
        ("goldDiscount", "goldDiscount"),
    )

    account = models.ForeignKey(Account, on_delete=models.DO_NOTHING)
    rule = models.CharField(choices=RULES_CHOICES, max_length=50)
    created_at = models.DateTimeField(default=timezone.now)
    expire_at = models.DateTimeField()
    is_expire = models.BooleanField(default=False)

    def __str__(self):
        return self.account.user.username
