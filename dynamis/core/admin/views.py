from django.views.generic import (
    TemplateView,
)

from dynamis.utils.mixins import (
    AdminRequired
)


class AdminIndexView(AdminRequired, TemplateView):
    template_name = 'admin/admin_index.html'
