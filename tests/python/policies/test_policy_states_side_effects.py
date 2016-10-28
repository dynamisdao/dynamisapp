import json

from constance import config

from dynamis.apps.payments.models import WAIT_FOR_TX_STATUS_RECEIVED
from dynamis.apps.policy.models import POLICY_STATUS_INIT, POLICY_STATUS_SUBMITTED, \
    POLICY_STATUS_ON_SMART_DEPOSIT_REFUND, POLICY_STATUS_ON_P2P_REVIEW, POLICY_STATUS_ON_RISK_ASSESSMENT_REVIEW, \
    POLICY_STATUS_APPROVED, POLICY_STATUS_ACTIVE, POLICY_STATUS_WAIT_FOR_PREMIUM, RiskAssessmentTask, \
    POLICY_STATUS_ON_COMPLETENESS_CHECK


def test_to_deposit_refund(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=POLICY_STATUS_SUBMITTED, cost_dollar=200, amount=10)
    policy.to_deposit_refund()
    assert policy.rejected_count == 1


def test_p2p_review_to_completeness_check_review_lack_of_assessors(factories):
    user = factories.UserFactory()

    user_2 = factories.UserFactory(is_risk_assessor=True)
    user_3 = factories.UserFactory(is_risk_assessor=True)
    user_4 = factories.UserFactory(is_risk_assessor=True)

    policy = factories.PolicyApplicationFactory(user=user)

    deposit = factories.SmartDepositFactory(policy=policy, state=POLICY_STATUS_SUBMITTED)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy, is_finished=True)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')

    policy.p2p_review_to_completeness_check()
    assert policy.state == POLICY_STATUS_ON_COMPLETENESS_CHECK

    assert RiskAssessmentTask.objects.all().count() == 3


def test_p2p_review_to_completeness_check_review_user_is_assessor(factories):
    user = factories.UserFactory(is_risk_assessor=True)
    user_2 = factories.UserFactory(is_risk_assessor=True)
    user_3 = factories.UserFactory(is_risk_assessor=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=POLICY_STATUS_SUBMITTED)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy, is_finished=True)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')

    policy.p2p_review_to_completeness_check()
    assert policy.state == POLICY_STATUS_ON_COMPLETENESS_CHECK

    assert RiskAssessmentTask.objects.all().count() == 2
    assert RiskAssessmentTask.objects.filter(user=user).exists() is False


def test_p2p_review_to_completeness_check_review_enough_assessors(factories):
    user = factories.UserFactory()

    user_2 = factories.UserFactory(is_risk_assessor=True)
    user_3 = factories.UserFactory(is_risk_assessor=True)
    user_4 = factories.UserFactory(is_risk_assessor=True)

    user_5 = factories.UserFactory(is_risk_assessor=True)
    user_6 = factories.UserFactory(is_risk_assessor=True)
    user_7 = factories.UserFactory(is_risk_assessor=True)

    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=POLICY_STATUS_SUBMITTED)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy, is_finished=True)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')

    policy.p2p_review_to_completeness_check()
    assert policy.state == POLICY_STATUS_ON_COMPLETENESS_CHECK

    assert RiskAssessmentTask.objects.all().count() == config.RISK_ASSESSORS_PER_POLICY_COUNT


def test_p2p_review_to_completeness_check_review_random_assessors(factories):
    user = factories.UserFactory()
    user_0 = factories.UserFactory()

    user_2 = factories.UserFactory(is_risk_assessor=True)
    user_3 = factories.UserFactory(is_risk_assessor=True)
    user_4 = factories.UserFactory(is_risk_assessor=True)

    user_5 = factories.UserFactory(is_risk_assessor=True)
    user_6 = factories.UserFactory(is_risk_assessor=True)
    user_7 = factories.UserFactory(is_risk_assessor=True)

    user_8 = factories.UserFactory(is_risk_assessor=True)
    user_9 = factories.UserFactory(is_risk_assessor=True)
    user_10 = factories.UserFactory(is_risk_assessor=True)

    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=POLICY_STATUS_SUBMITTED)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy, is_finished=True)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')

    policy_2 = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                  user=user_0)
    deposit_2 = factories.SmartDepositFactory(policy=policy_2, state=POLICY_STATUS_SUBMITTED)
    app_item_2 = factories.IdentityApplicationItemFactory(policy_application=policy_2, is_finished=True)
    factories.IdentityPeerReviewFactory(application_item=app_item_2, result='3')

    policy.p2p_review_to_completeness_check()
    assert policy.state == POLICY_STATUS_ON_COMPLETENESS_CHECK

    policy_2.p2p_review_to_completeness_check()
    assert policy.state == POLICY_STATUS_ON_COMPLETENESS_CHECK

    assert RiskAssessmentTask.objects.all().count() == config.RISK_ASSESSORS_PER_POLICY_COUNT * 2

    first_assessors = RiskAssessmentTask.objects.filter(policy=policy).values_list('user__id', flat=True)
    second_assessors = RiskAssessmentTask.objects.filter(policy=policy_2).values_list('user__id', flat=True)

    assert sorted(first_assessors) != sorted(second_assessors)


def test_p2p_review_to_completeness_check_already_created(factories):
    user = factories.UserFactory()
    user_assessor = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_ON_P2P_REVIEW,
                                                user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=POLICY_STATUS_SUBMITTED)
    app_item = factories.IdentityApplicationItemFactory(policy_application=policy, is_finished=True)
    factories.IdentityPeerReviewFactory(application_item=app_item, result='3')

    factories.RiskAssessmentTaskFactory.create_batch(5, policy=policy)
    assert RiskAssessmentTask.objects.all().count() == 5

    policy.p2p_review_to_completeness_check()
    assert policy.state == POLICY_STATUS_ON_COMPLETENESS_CHECK

    assert RiskAssessmentTask.objects.all().count() == 5


def test_submit_to_p2p_review(factories, policy_data, job_data):
    policy_data['identity']['verification_data']['proofs'].append({'dummy': 'data'})
    policy_data['employmentHistory']['jobs'].append(job_data)

    user = factories.UserFactory(is_risk_assessor=True)
    user_2 = factories.UserFactory(is_risk_assessor=True)
    user_3 = factories.UserFactory(is_risk_assessor=True)
    policy = factories.PolicyApplicationFactory(state=POLICY_STATUS_SUBMITTED,
                                                user=user,
                                                data=json.dumps({'policy_data': policy_data}))
    deposit = factories.SmartDepositFactory(policy=policy, state=WAIT_FOR_TX_STATUS_RECEIVED,
                                            cost_dollar=(20 * config.DOLLAR_ETH_EXCHANGE_RATE), amount=20)

    policy.submit_to_p2p_review()
    assert policy.state == POLICY_STATUS_ON_P2P_REVIEW
    assert policy.review_tasks.count() == 2
