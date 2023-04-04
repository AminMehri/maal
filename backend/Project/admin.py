from django.contrib import admin
from Project.models import Project, AcceptedProject


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'admin_confirmed', 'total_price', 'price', 'fee_percent', 'categories', 'is_full', 'publish')

admin.site.register(Project, ProjectAdmin)


class AcceptedProjectAdmin(admin.ModelAdmin):
    list_display = ('project', 'freelancer', 'pending', 'price', 'followers', 'following', 'engagement')

admin.site.register(AcceptedProject, AcceptedProjectAdmin)

