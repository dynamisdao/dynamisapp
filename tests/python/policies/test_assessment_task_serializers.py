import pytest
from constance import config
from rest_framework.exceptions import ValidationError

from dynamis.apps.policy.api.v1.serializers import RiskAssessmentTaskDetailUserSerializer, \
    RiskAssessmentTaskShortSerializer, \
    RiskAssessmentTaskDetailAdminSerializer, RiskAssessmentTaskDetailBaseSerializer


def test_risk_assessment_task_detail_serializer(factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    data = {
        'id': risk_assessment_task.id,
        'policyid': risk_assessment_task.policy.pk,
        'is_finished': risk_assessment_task.is_finished,
        'bet1': risk_assessment_task.bet1,
        'bet2': risk_assessment_task.bet2,
        'question1': risk_assessment_task.question1,
        'question2': risk_assessment_task.question2,
    }

    serializer = RiskAssessmentTaskDetailUserSerializer(instance=risk_assessment_task)
    assert serializer.data == data


def test_risk_assessment_task_detail_user_serializer_update(factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    data_request = {
        'id': risk_assessment_task.id,
        'policyid': risk_assessment_task.policy.pk,
        'is_finished': risk_assessment_task.is_finished,
        'bet1': config.BET_MIN_AMOUNT_USER,
        'bet2': config.BET_MIN_AMOUNT_USER,
        'question1': config.MONTHS_PAY_PREMIUMS_BEFORE_OPENING_A_CLAIM_MAX,
        'question2': config.WEEKS_PAID_FOR_FIRST_CLAIM_MAX,
    }

    data_return = {
        'is_finished': risk_assessment_task.is_finished,
        'bet1': config.BET_MIN_AMOUNT_USER,
        'bet2': config.BET_MIN_AMOUNT_USER,
        'question1': config.MONTHS_PAY_PREMIUMS_BEFORE_OPENING_A_CLAIM_MAX,
        'question2': config.WEEKS_PAID_FOR_FIRST_CLAIM_MAX,
    }

    serializer = RiskAssessmentTaskDetailUserSerializer(data=data_request)
    assert serializer.is_valid() is True
    assert serializer.data == data_return


def test_risk_assessment_task_detail_user_serializer_update_exception(factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    data_request = {
        'id': risk_assessment_task.id,
        'policyid': risk_assessment_task.policy.pk,
        'is_finished': risk_assessment_task.is_finished,
        'bet1': config.BET_MAX_AMOUNT_USER,
        'bet2': config.BET_MAX_AMOUNT_USER + 1,
        'question1': config.MONTHS_PAY_PREMIUMS_BEFORE_OPENING_A_CLAIM_MAX,
        'question2': config.WEEKS_PAID_FOR_FIRST_CLAIM_MAX,
    }

    serializer = RiskAssessmentTaskDetailUserSerializer(data=data_request)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


def test_risk_assessment_task_detail_admin_serializer_update(factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    data_request = {
        'id': risk_assessment_task.id,
        'policyid': risk_assessment_task.policy.pk,
        'is_finished': risk_assessment_task.is_finished,
        'bet1': config.BET_MIN_AMOUNT_ADMIN,
        'bet2': config.BET_MIN_AMOUNT_ADMIN,
        'question1': config.MONTHS_PAY_PREMIUMS_BEFORE_OPENING_A_CLAIM_MAX,
        'question2': config.WEEKS_PAID_FOR_FIRST_CLAIM_MAX,
    }

    data_return = {
        'is_finished': risk_assessment_task.is_finished,
        'bet1': config.BET_MIN_AMOUNT_ADMIN,
        'bet2': config.BET_MIN_AMOUNT_ADMIN,
        'question1': config.MONTHS_PAY_PREMIUMS_BEFORE_OPENING_A_CLAIM_MAX,
        'question2': config.WEEKS_PAID_FOR_FIRST_CLAIM_MAX,
    }

    serializer = RiskAssessmentTaskDetailAdminSerializer(data=data_request)
    assert serializer.is_valid() is True
    assert serializer.data == data_return


def test_risk_assessment_task_detail_admin_serializer_update_exception(factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    data_request = {
        'id': risk_assessment_task.id,
        'policyid': risk_assessment_task.policy.pk,
        'is_finished': risk_assessment_task.is_finished,
        'bet1': config.BET_MAX_AMOUNT_ADMIN,
        'bet2': config.BET_MAX_AMOUNT_ADMIN + 1,
        'question1': config.MONTHS_PAY_PREMIUMS_BEFORE_OPENING_A_CLAIM_MAX,
        'question2': config.WEEKS_PAID_FOR_FIRST_CLAIM_MAX,
    }

    serializer = RiskAssessmentTaskDetailAdminSerializer(data=data_request)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


def test_risk_assessment_task_detail_base_serializer_update_exception_question_one(factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    data_request = {
        'id': risk_assessment_task.id,
        'policyid': risk_assessment_task.policy.pk,
        'is_finished': risk_assessment_task.is_finished,
        'question1': config.MONTHS_PAY_PREMIUMS_BEFORE_OPENING_A_CLAIM_MAX + 1,
        'question2': config.WEEKS_PAID_FOR_FIRST_CLAIM_MAX,
    }

    serializer = RiskAssessmentTaskDetailBaseSerializer(data=data_request)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


def test_risk_assessment_task_detail_base_serializer_update_exception_question_two(factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    data_request = {
        'id': risk_assessment_task.id,
        'policyid': risk_assessment_task.policy.pk,
        'is_finished': risk_assessment_task.is_finished,
        'question1': config.MONTHS_PAY_PREMIUMS_BEFORE_OPENING_A_CLAIM_MAX,
        'question2': config.WEEKS_PAID_FOR_FIRST_CLAIM_MAX + 1,
    }

    serializer = RiskAssessmentTaskDetailBaseSerializer(data=data_request)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)


def test_risk_assessment_task_short_serializer(factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    data = {
        'id': risk_assessment_task.id,
        'is_finished': risk_assessment_task.is_finished,
    }

    serializer = RiskAssessmentTaskShortSerializer(data)
    assert serializer.data == data
