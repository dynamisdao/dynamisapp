from django.contrib import admin
from models import User, AccountConfig


class UserAdmin(admin.ModelAdmin):
    pass


class AccountConfigAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(AccountConfig, AccountConfigAdmin)

