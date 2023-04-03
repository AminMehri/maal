from django.contrib import admin
from Account.models import User, Account, InstagramAccount, Freelancer,Rule

admin.site.register(User)
admin.site.register(Account)
admin.site.register(InstagramAccount)
admin.site.register(Freelancer)
admin.site.register(Rule)
