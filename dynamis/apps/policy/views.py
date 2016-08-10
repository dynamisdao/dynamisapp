from django.views.generic import (
    TemplateView,
    DetailView,
)

from dynamis.utils.mixins import LoginRequired


class PolicyCreateView(DetailView):
    template_name = "policies/policy_create.html"
    context_object_name = "policy"

    def get_object(self):
        if self.request.user.is_authenticated():
            return self.request.user.policies.first()
        else:
            return None


class PolicyEditView(LoginRequired, DetailView):
    template_name = "policies/policy_create.html"
    context_object_name = "policy"

    def get_object(self):
        return self.request.user.policies.get(pk=self.kwargs['pk'])


class PeerReviewItemsView(LoginRequired, TemplateView):
    template_name = "policies/peer_review.html"
