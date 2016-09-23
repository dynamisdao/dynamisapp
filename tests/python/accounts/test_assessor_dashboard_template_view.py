from django.core.urlresolvers import reverse

from rest_framework import status


def test_assessor_dashboard_template_view(user_webtest_client, factories):
    policy = factories.PolicyApplicationFactory(user=user_webtest_client.user)
    risk_assessment = factories.RiskAssessmentTaskFactory(user=user_webtest_client.user, policy=policy)

    url = reverse('assessor-dashboard')

    response = user_webtest_client.get(url)

    assert response.status_code == status.HTTP_200_OK
