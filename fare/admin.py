from django.contrib import admin
from .models import User_Transaction_history, User_amount,Scanned

# Registering multiple models at once
admin.site.register([User_Transaction_history])

# Customizing the admin interface for User_amount
class User_amountAdmin(admin.ModelAdmin):  # Inherit from admin.ModelAdmin
    list_display = ['user', 'amount', 'last_transaction']

# Registering User_amount with the custom admin class
admin.site.register(User_amount, User_amountAdmin)


class ScannedAdmin(admin.ModelAdmin):  # Inherit from admin.ModelAdmin
    list_display = ['user', 'gps_id', 'scanned_datetime']
admin.site.register(Scanned, ScannedAdmin)
