from django.contrib import admin
from Admin.models import Admin



class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin_rule')

admin.site.register(Admin, AdminAdmin)
