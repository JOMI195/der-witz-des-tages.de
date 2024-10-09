from django.contrib import admin

from .models import Account


class AccountInline(admin.TabularInline):
    model = Account
    list_display = ["recieves_newsletter"]
    extra = 0
    max_num = 1


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    model = Account
