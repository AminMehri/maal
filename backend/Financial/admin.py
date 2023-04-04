from django.contrib import admin
from Financial.models import Withdraw, Deposit
# Register your models here.


class WithdrawAdmin(admin.ModelAdmin):
    list_display = ('freelancer', 'is_paid', 'paid_by', 'amount')

admin.site.register(Withdraw, WithdrawAdmin)
admin.site.register(Deposit)
