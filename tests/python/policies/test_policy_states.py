import datetime
import pytest
from django_fsm import TransitionNotAllowed

from dynamis.apps.policy.models import POLICY_STATUS_INIT, POLICY_STATUS_SUBMITTED, \
    POLICY_STATUS_ON_SMART_DEPOSIT_REFUND, POLICY_STATUS_ON_P2P_REVIEW, POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW, \
    POLICY_STATUS_APPROVED, POLICY_STATUS_ACTIVE, POLICY_STATUS_WAIT_FOR_PREMIUM


def test_deny_change_policy_state_directly(factories):
    policy = factories.PolicyApplicationFactory()
    assert policy.state == POLICY_STATUS_INIT

    with pytest.raises(AttributeError):
        policy.state = POLICY_STATUS_SUBMITTED
    assert policy.state == POLICY_STATUS_INIT


def test_policy_submission(factories):
    policy = factories.PolicyApplicationFactory()

    assert policy.state == POLICY_STATUS_INIT
    policy.submit()
    assert policy.state == POLICY_STATUS_SUBMITTED


def test_policy_cancel_submission(factories):
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_SUBMITTED)
    policy.cancel_submission()
    assert policy.state == POLICY_STATUS_INIT


def test_to_deposit_refund(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(user=user)
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy.to_deposit_refund()
    assert policy.state == POLICY_STATUS_ON_SMART_DEPOSIT_REFUND
    assert policy.rejected_count == 1


def test_to_deposit_refund_no_deposit(factories):
    policy = factories.PolicyApplicationFactory()
    with pytest.raises(TransitionNotAllowed):
        policy.to_deposit_refund()
    assert policy.state == POLICY_STATUS_INIT
    assert policy.rejected_count == 0


def test_deposit_refund_to_init(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True, refunded=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_SMART_DEPOSIT_REFUND,
                                                user=user)
    policy.deposit_refund_to_init()
    assert policy.state == POLICY_STATUS_INIT


def test_deposit_refund_to_init_not_refunded(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True, refunded=False)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_SMART_DEPOSIT_REFUND,
                                                user=user)
    with pytest.raises(TransitionNotAllowed):
        policy.deposit_refund_to_init()
    assert policy.state == POLICY_STATUS_ON_SMART_DEPOSIT_REFUND


def test_submit_to_p2p_review(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_SUBMITTED,
                                                user=user)
    policy.submit_to_p2p_review()
    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW


def test_submit_to_p2p_review_deposit_refunded(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True, refunded=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_SUBMITTED,
                                                user=user)
    with pytest.raises(TransitionNotAllowed):
        policy.submit_to_p2p_review()
    assert policy.state == POLICY_STATUS_SUBMITTED


def test_p2p_review_to_risk_assessment_review_int_result(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')

    policy.p2p_review_to_risk_assessment_review()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_p2p_review_to_risk_assessment_review_str_result(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='verified')

    policy.p2p_review_to_risk_assessment_review()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_p2p_review_to_risk_assessment_review_falsified_result(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='falsified')

    with pytest.raises(TransitionNotAllowed):
        policy.p2p_review_to_risk_assessment_review()
    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW


def test_p2p_review_to_risk_assessment_review_low_result(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='2')

    with pytest.raises(TransitionNotAllowed):
        policy.p2p_review_to_risk_assessment_review()
    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW


def test_risk_assessment_review_to_approved(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=True)
    policy.risk_assessment_review_to_approved()
    assert policy.state == POLICY_STATUS_APPROVED


def test_risk_assessment_review_to_approved_no_tasks(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    with pytest.raises(TransitionNotAllowed):
        policy.risk_assessment_review_to_approved()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_risk_assessment_review_to_approved_not_all_tasks_finished(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=True)
    risk_assessment_task_2 = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=False)
    with pytest.raises(TransitionNotAllowed):
        policy.risk_assessment_review_to_approved()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_activate_policy(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=True)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')
    factories.PremiumPaymentFactory(user=user, is_confirmed=True)
    policy.activate()
    assert policy.state == POLICY_STATUS_ACTIVE


def test_activate_no_premium(factories):
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=True)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')
    with pytest.raises(TransitionNotAllowed):
        policy.activate()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_activate_too_old_premium(factories):
    old_date = datetime.datetime.now() - datetime.timedelta(weeks=5)
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=True)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')
    premium = factories.PremiumPaymentFactory(user=user, is_confirmed=True)
    premium.created_at = old_date
    premium.save()
    with pytest.raises(TransitionNotAllowed):
        policy.activate()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_wait_for_premium(factories):
    new_date = datetime.datetime.now() - datetime.timedelta(weeks=6)
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ACTIVE,
                                                user=user)
    premium = factories.PremiumPaymentFactory(user=user, is_confirmed=True)
    premium.created_at = new_date
    premium.save()
    policy.wait_for_payment()
    assert policy.state == POLICY_STATUS_WAIT_FOR_PREMIUM


def test_wait_for_premium_too_new_premium(factories):
    new_date = datetime.datetime.now() - datetime.timedelta(weeks=1)
    user = factories.UserFactory()
    deposit = factories.SmartDepositFactory(user=user, is_confirmed=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ACTIVE,
                                                user=user)
    premium = factories.PremiumPaymentFactory(user=user, is_confirmed=True)
    premium.created_at = new_date
    premium.save()
    with pytest.raises(TransitionNotAllowed):
        policy.wait_for_payment()
    assert policy.state == POLICY_STATUS_ACTIVE
