from django.core.urlresolvers import reverse_lazy


URLS = {
    'user-profile': reverse_lazy('user-profile'),
    'account-create': reverse_lazy('v1:account-create'),
    'policy-create': reverse_lazy('v1:policy-list'),
    'application-item-list': reverse_lazy('v1:application-item-list'),
    'peer-review-history': reverse_lazy('v1:peer-review-history-list'),
    'verify-keybase': reverse_lazy('v1:verify-keybase'),
    'my-policy': reverse_lazy('my-policy'),
}


def api_urls(request):
    return {'api_urls': URLS}
