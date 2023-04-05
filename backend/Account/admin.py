from django.contrib import admin
from Account.models import User, Account, InstagramAccount, Freelancer,Rule

admin.site.register(User)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')

admin.site.register(Account, AccountAdmin)



admin.site.register(InstagramAccount)

# class FreelancerAdmin(admin.ModelAdmin):
#     list_display = ('account', 'is_accepted', 'verified_by', 'reject_reason')

admin.site.register(Freelancer)


admin.site.register(Rule)
