from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages

from django_tables2 import SingleTableMixin

from django_filters.views import FilterMixin

from django.views.generic import (
    ListView,
    UpdateView,
)

from dynamis.apps.policy.models import PolicyApplication
from dynamis.utils.mixins import (
    AdminRequired
)

from .tables import UserTable, PolicyTable
from .forms import UserUpdateForm
from .filters import UserFilter, PolicyFilter

User = get_user_model()


class BaseIndexViewMixin(object):
    def get_context_data(self, **kwargs):
        filterset = self.get_filterset(self.get_filterset_class())
        kwargs['filter'] = filterset
        kwargs['object_list'] = filterset.qs
        self.object_list = filterset.qs
        context = super(BaseIndexViewMixin, self).get_context_data(**kwargs)
        return context


class UserIndexView(AdminRequired, SingleTableMixin, FilterMixin, ListView, BaseIndexViewMixin):
    queryset = User.objects.all()
    template_name = 'accounts/admin/user_index.html'
    table_class = UserTable
    table_pagination = {
        'per_page': 20,
    }
    filterset_class = UserFilter


class PolicyIndexViewMixin(AdminRequired, SingleTableMixin, FilterMixin, ListView, BaseIndexViewMixin):
    queryset = PolicyApplication.objects.all()
    template_name = 'accounts/admin/policy_index.html'
    table_class = PolicyTable
    table_pagination = {
        'per_page': 20,
    }
    filterset_class = PolicyFilter


class UserUpdateView(AdminRequired, UpdateView):
    queryset = User.objects.all()
    context_object_name = 'dynamis_user'
    template_name = 'accounts/admin/user_detail.html'
    form_class = UserUpdateForm

    def form_valid(self, form):
        messages.info(self.request, "User updated")
        return super(UserUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('admin:user-detail', kwargs=self.kwargs)
