from rest_framework import status
from rest_framework.status import is_success


class DisableCSRFMiddleWare(object):
    def process_request(self, request):
            setattr(request, '_dont_enforce_csrf_checks', True)


class ReplaceResponseCodesMiddleWare(object):

    def process_response(self, request, response):
        if response.status_code != 200 and is_success(response.status_code):
            response.status_code = status.HTTP_200_OK
        return response
