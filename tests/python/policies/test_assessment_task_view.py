from constance import config
from rest_framework import status
from rest_framework.reverse import reverse

from dynamis.apps.payments.models import MakeBetOperation
from dynamis.apps.policy.api.v1.serializers import RiskAssessmentTaskDetailUserSerializer, RiskAssessmentTaskShortSerializer
from dynamis.apps.policy.models import RiskAssessmentTask


def test_get_my_assessment_tasks_list(user_webtest_client, api_client, factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user_webtest_client.user)
    risk_assessment_task_2 = factories.RiskAssessmentTaskFactory(user=user_webtest_client.user)

    other_user = factories.UserFactory()
    risk_assessment_task_3_not_my = factories.RiskAssessmentTaskFactory(user=other_user)

    url = reverse('v1:assessment_tasks-list')

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 2
    assert response.data['results'][0] == RiskAssessmentTaskShortSerializer(risk_assessment_task).data
    assert response.data['results'][1] == RiskAssessmentTaskShortSerializer(risk_assessment_task_2).data


def test_get_all_assessment_tasks_list_admin(user_webtest_client, api_client, factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user_webtest_client.user)
    risk_assessment_task_2 = factories.RiskAssessmentTaskFactory(user=user_webtest_client.user)

    other_user = factories.UserFactory()
    risk_assessment_task_3 = factories.RiskAssessmentTaskFactory(user=other_user)

    user_admin = factories.UserFactory(is_staff=True)
    api_client.force_authenticate(user_admin)

    url = reverse('v1:assessment_tasks-list')

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 3
    assert response.data['results'][0] == RiskAssessmentTaskShortSerializer(risk_assessment_task).data
    assert response.data['results'][1] == RiskAssessmentTaskShortSerializer(risk_assessment_task_2).data
    assert response.data['results'][2] == RiskAssessmentTaskShortSerializer(risk_assessment_task_3).data


def test_get_assessment_tasks_list_unauthorized(user_webtest_client, api_client, factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user_webtest_client.user)
    risk_assessment_task_2 = factories.RiskAssessmentTaskFactory(user=user_webtest_client.user)

    api_client.force_authenticate(None)

    url = reverse('v1:assessment_tasks-list')

    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_unauthorized(api_client, factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()
    url = reverse('v1:assessment_tasks-detail', args=[risk_assessment_task.pk])

    response = api_client.get(url)
    api_client.force_authenticate(None)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_my_assessment_task(user_webtest_client, api_client, factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user_webtest_client.user)
    url = reverse('v1:assessment_tasks-detail', args=[risk_assessment_task.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == RiskAssessmentTaskDetailUserSerializer(risk_assessment_task).data


def test_get_other_task_if_admin(api_client, factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    user_admin = factories.UserFactory(is_staff=True)
    api_client.force_authenticate(user_admin)

    url = reverse('v1:assessment_tasks-detail', args=[risk_assessment_task.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == RiskAssessmentTaskDetailUserSerializer(risk_assessment_task).data


def test_get_other_task_if_not_admin(api_client, factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    user_not_admin = factories.UserFactory(is_staff=False)
    api_client.force_authenticate(user_not_admin)

    url = reverse('v1:assessment_tasks-detail', args=[risk_assessment_task.pk])

    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_my_task(user_webtest_client, api_client, factories, internal_contractor):
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user_webtest_client.user)

    user_token_amount = 50
    user_token_account = factories.TokenAccountFactory(user=user_webtest_client.user,
                                                       immature_tokens_balance=user_token_amount)

    contractor_token_account = factories.TokenAccountFactory(user=internal_contractor)

    data_to_update = {
        'bet1': config.BET_MAX_AMOUNT_USER,
        'bet2': config.BET_MAX_AMOUNT_USER,
        'is_finished': True
    }

    url = reverse('v1:assessment_tasks-detail', args=[risk_assessment_task.pk])

    response = api_client.put(url, data=data_to_update)

    amount = data_to_update['bet1'] + data_to_update['bet2']

    assert response.status_code == status.HTTP_200_OK
    assert RiskAssessmentTask.objects.get().bet1 == config.BET_MAX_AMOUNT_USER
    assert RiskAssessmentTask.objects.get().bet2 == config.BET_MAX_AMOUNT_USER
    assert RiskAssessmentTask.objects.get().is_finished is True

    bet_operation = MakeBetOperation.objects.get()
    assert bet_operation.assessor_token_account.user == risk_assessment_task.user
    assert bet_operation.internal_contractor_token_account.user == internal_contractor
    assert bet_operation.risk_assessment_task == risk_assessment_task
    assert bet_operation.amount == amount

    contractor_token_account.refresh_from_db()
    assert contractor_token_account.immature_tokens_balance == amount
    user_token_account.refresh_from_db()
    assert user_token_account.immature_tokens_balance == user_token_amount - amount
    risk_assessment_task.refresh_from_db()
    assert risk_assessment_task.is_finished is True


def test_update_other_task_if_admin(user_webtest_client, api_client, factories, internal_contractor):
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user_webtest_client.user)

    user_token_amount = 50
    user_token_account = factories.TokenAccountFactory(user=user_webtest_client.user,
                                                       immature_tokens_balance=user_token_amount)

    user_admin = factories.UserFactory(is_staff=True)
    api_client.force_authenticate(user_admin)

    data_to_update = {
        'bet1': config.BET_MAX_AMOUNT_ADMIN,
        'bet2': config.BET_MAX_AMOUNT_ADMIN,
        'is_finished': True
    }

    url = reverse('v1:assessment_tasks-detail', args=[risk_assessment_task.pk])

    response = api_client.put(url, data=data_to_update)

    assert response.status_code == status.HTTP_200_OK
    assert RiskAssessmentTask.objects.get().bet1 == config.BET_MAX_AMOUNT_ADMIN
    assert RiskAssessmentTask.objects.get().bet2 == config.BET_MAX_AMOUNT_ADMIN
    assert RiskAssessmentTask.objects.get().is_finished is True

    bet_operation = MakeBetOperation.objects.get()
    assert bet_operation.assessor_token_account.user == risk_assessment_task.user
    assert bet_operation.internal_contractor_token_account.user == internal_contractor
    assert bet_operation.risk_assessment_task == risk_assessment_task
    assert bet_operation.amount == config.BET_MAX_AMOUNT_ADMIN + config.BET_MAX_AMOUNT_ADMIN

    risk_assessment_task.refresh_from_db()
    assert risk_assessment_task.is_finished is True


def test_update_other_task(user_webtest_client, api_client, factories):
    other_user = factories.UserFactory()
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=other_user)

    data_to_update = {
        'bet1': 5.2,
        'bet2': 8.2,
        'is_finished': True
    }

    url = reverse('v1:assessment_tasks-detail', args=[risk_assessment_task.pk])

    response = api_client.put(url, data=data_to_update)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert RiskAssessmentTask.objects.get().bet1 != 5.2
    assert RiskAssessmentTask.objects.get().bet2 != 8.2
    assert RiskAssessmentTask.objects.get().is_finished is not True


def test_update_other_task_unauthorized(user_webtest_client, api_client, factories):
    other_user = factories.UserFactory()
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=other_user)

    api_client.force_authenticate(None)

    data_to_update = {
        'bet1': 5.2,
        'bet2': 8.2,
        'is_finished': True
    }

    url = reverse('v1:assessment_tasks-detail', args=[risk_assessment_task.pk])

    response = api_client.put(url, data=data_to_update)

    assert response.status_code == status.HTTP_403_FORBIDDEN
