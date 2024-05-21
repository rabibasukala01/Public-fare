from django.contrib import admin

# Register your models here.
from .models import Bank

class BankAdmin(admin.ModelAdmin):
    exclude = ('account_number',)
    list_display = ('fullname', 'account_number','email', 'phone', 'amount', 'nagrita_no', 'created_at', 'updated_at')

admin.site.register(Bank, BankAdmin)