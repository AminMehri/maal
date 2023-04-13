from django.contrib import admin
from Ticket.models import Ticket, Conversation, AdminAnswer


class ConversationAdmin(admin.ModelAdmin):
    list_display = ('account', 'subject', 'status')

admin.site.register(Conversation, ConversationAdmin)


class TicketAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'text')

admin.site.register(Ticket, TicketAdmin)


class AdminAwnserAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'admin', 'text')

admin.site.register(AdminAnswer, AdminAwnserAdmin)