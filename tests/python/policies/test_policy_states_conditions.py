import datetime
import json

import pytest
from django_fsm import TransitionNotAllowed

from dynamis.apps.policy.models import POLICY_STATUS_INIT, POLICY_STATUS_SUBMITTED, \
    POLICY_STATUS_ON_SMART_DEPOSIT_REFUND, POLICY_STATUS_ON_P2P_REVIEW, POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW, \
    POLICY_STATUS_APPROVED, POLICY_STATUS_ACTIVE, POLICY_STATUS_WAIT_FOR_PREMIUM, POLICY_STATUS_ON_COMPLETENESS_CHECK
from dynamis.settings import DEBUG


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
    eth_account = factories.EthAccountFactory(user=user)
    policy = factories.PolicyApplicationFactory(user=user)
    deposit = factories.SmartDepositFactory(policy=policy, eth_account=eth_account, state=2, coast_dollar=200,
                                            amount=20)
    policy.to_deposit_refund()
    assert policy.state == POLICY_STATUS_ON_SMART_DEPOSIT_REFUND


def test_to_deposit_refund_no_deposit(factories):
    policy = factories.PolicyApplicationFactory()
    with pytest.raises(TransitionNotAllowed):
        policy.to_deposit_refund()
    assert policy.state == POLICY_STATUS_INIT
    assert policy.rejected_count == 0


def test_deposit_refund_to_init(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_SMART_DEPOSIT_REFUND,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    deposit_refund = factories.SmartDepositRefundFactory(smart_deposit=deposit, is_confirmed=True)
    policy.deposit_refund_to_init()
    assert policy.state == POLICY_STATUS_INIT


def test_deposit_refund_to_init_not_refunded(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_SMART_DEPOSIT_REFUND,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    with pytest.raises(TransitionNotAllowed):
        policy.deposit_refund_to_init()
    assert policy.state == POLICY_STATUS_ON_SMART_DEPOSIT_REFUND


def test_submit_to_p2p_review_ok(factories, policy_data, job_data):
    user = factories.UserFactory()
    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_SUBMITTED,
                                                user=user,
                                                data=json.dumps({'policy_data': policy_data}))
    deposit = factories.SmartDepositFactory(policy=policy, state=2, coast_dollar=200, amount=20)
    policy.submit_to_p2p_review()
    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW


def test_submit_to_p2p_review_small_amount(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_SUBMITTED,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2, coast_dollar=200, amount=1)
    with pytest.raises(TransitionNotAllowed):
        policy.submit_to_p2p_review()
    assert policy.state == POLICY_STATUS_SUBMITTED


def test_submit_to_p2p_review_deposit_refunded(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_SUBMITTED,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2, coast_dollar=200, amount=10)
    deposit_refund = factories.SmartDepositRefundFactory(smart_deposit=deposit, is_confirmed=True)
    with pytest.raises(TransitionNotAllowed):
        policy.submit_to_p2p_review()
    assert policy.state == POLICY_STATUS_SUBMITTED


def test_p2p_review_to_completeness_check_int_result(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')

    policy.p2p_review_to_completeness_check()
    assert policy.state == POLICY_STATUS_ON_COMPLETENESS_CHECK


def test_p2p_review_to_completeness_check_str_result(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='verified')

    policy.p2p_review_to_completeness_check()
    assert policy.state == POLICY_STATUS_ON_COMPLETENESS_CHECK


def test_p2p_review_to_completeness_check_falsified_result(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='falsified')

    with pytest.raises(TransitionNotAllowed):
        policy.p2p_review_to_completeness_check()
    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW


def test_p2p_review_to_completeness_check_low_result(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='2')

    with pytest.raises(TransitionNotAllowed):
        policy.p2p_review_to_completeness_check()
    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW


def test_completeness_check_to_assessment_review_false(factories):
    # TODO remove 'if not debug' when we complete develop and will test all states
    if not DEBUG:
        user = factories.UserFactory()
        policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_COMPLETENESS_CHECK,
                                                    user=user, is_completeness_checked=False)

        with pytest.raises(TransitionNotAllowed):
            policy.completeness_check_to_risk_assessment_review()
        assert policy.state == POLICY_STATUS_ON_COMPLETENESS_CHECK


def test_completeness_check_to_assessment_review_true(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_COMPLETENESS_CHECK,
                                                user=user, is_completeness_checked=True)
    policy.completeness_check_to_risk_assessment_review()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_risk_assessment_review_to_approved(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=True)
    policy.risk_assessment_review_to_approved()
    assert policy.state == POLICY_STATUS_APPROVED


def test_risk_assessment_review_to_approved_no_tasks(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    with pytest.raises(TransitionNotAllowed):
        policy.risk_assessment_review_to_approved()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_risk_assessment_review_to_approved_not_all_tasks_finished(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=True)
    risk_assessment_task_2 = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=False)
    with pytest.raises(TransitionNotAllowed):
        policy.risk_assessment_review_to_approved()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_activate_policy(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2, coast_dollar=200, amount=20)
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=True)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')
    eth_account = factories.EthAccountFactory(user=user)
    factories.PremiumPaymentFactory(eth_account=eth_account, is_confirmed=True)
    policy.activate()
    assert policy.state == POLICY_STATUS_ACTIVE


def test_activate_no_premium(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=True)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')
    with pytest.raises(TransitionNotAllowed):
        policy.activate()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_activate_too_old_premium(factories):
    old_date = datetime.datetime.now() - datetime.timedelta(weeks=5)
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    risk_assessment_task = factories.RiskAssessmentTaskFactory(user=user, policy=policy, is_finished=True)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')
    eth_account = factories.EthAccountFactory(user=user)
    premium = factories.PremiumPaymentFactory(eth_account=eth_account, is_confirmed=True)
    premium.created_at = old_date
    premium.save()
    with pytest.raises(TransitionNotAllowed):
        policy.activate()
    assert policy.state == POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW


def test_wait_for_premium(factories):
    new_date = datetime.datetime.now() - datetime.timedelta(weeks=6)
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ACTIVE,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    eth_account = factories.EthAccountFactory(user=user)
    premium = factories.PremiumPaymentFactory(eth_account=eth_account, is_confirmed=True)
    premium.created_at = new_date
    premium.save()
    policy.wait_for_payment()
    assert policy.state == POLICY_STATUS_WAIT_FOR_PREMIUM


def test_wait_for_premium_too_new_premium(factories):
    new_date = datetime.datetime.now() - datetime.timedelta(weeks=1)
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ACTIVE,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=2)
    eth_account = factories.EthAccountFactory(user=user)
    premium = factories.PremiumPaymentFactory(eth_account=eth_account, is_confirmed=True)
    premium.created_at = new_date
    premium.save()
    with pytest.raises(TransitionNotAllowed):
        policy.wait_for_payment()
    assert policy.state == POLICY_STATUS_ACTIVE
