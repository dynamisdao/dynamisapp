from django.contrib import admin

from dynamis.apps.policy.models import PolicyApplication, RiskAssessmentTask, ReviewTask


class PolicyApplicationAdmin(admin.ModelAdmin):
    pass


class RiskAssessmentTaskAdmin(admin.ModelAdmin):
    pass


class ApplicationItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(PolicyApplication, PolicyApplicationAdmin)
admin.site.register(RiskAssessmentTask, RiskAssessmentTaskAdmin)
admin.site.register(ReviewTask, ApplicationItemAdmin)
