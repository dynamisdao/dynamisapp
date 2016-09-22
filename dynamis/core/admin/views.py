from django.views.generic import (
    TemplateView,
)

from dynamis.utils.mixins import (
    AdminRequired
)


class AdminIndexView(AdminRequired, TemplateView):
    template_name = '_index.html'
