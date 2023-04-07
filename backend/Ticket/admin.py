from django.contrib import admin
from Ticket.models import Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user')

admin.site.register(Ticket, TicketAdmin)