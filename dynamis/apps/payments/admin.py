from django.contrib import admin

from dynamis.apps.payments.models import PremiumPayment, SmartDeposit


class PremiumPaymentAdmin(admin.ModelAdmin):
    pass


class SmartDepositAdmin(admin.ModelAdmin):
    pass


admin.site.register(PremiumPayment, PremiumPaymentAdmin)
admin.site.register(SmartDeposit, SmartDepositAdmin)
