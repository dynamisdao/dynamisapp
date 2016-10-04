import json
import factory

from dynamis.apps.policy.models import (
    PolicyApplication,
    ReviewTask,
    PeerReview,
    RiskAssessmentTask)


class PolicyApplicationFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('factories.accounts.UserFactory')
    is_final = False
    data = json.dumps({'field-a': 'A'})

    class Meta:
        model = PolicyApplication


class BaseApplicationItemFactory(factory.DjangoModelFactory):
    policy_application = factory.SubFactory('factories.policy.PolicyApplicationFactory')

    data = json.dumps({'field-a': 'A'})

    class Meta:
        model = ReviewTask


class IdentityApplicationItemFactory(BaseApplicationItemFactory):
    type = ReviewTask.TYPE_IDENTITY


class EmploymentClaimApplicationItemFactory(BaseApplicationItemFactory):
    type = ReviewTask.TYPE_EMPLOYMENT_CLAIM


class BasePeerReviewFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('factories.accounts.UserFactory')

    class Meta:
        model = PeerReview


class IdentityPeerReviewFactory(BasePeerReviewFactory):
    application_item = factory.SubFactory('factories.policy.IdentityApplicationItemFactory')
    data = json.dumps({'result': '1'})
    result = '1'


class EmploymentClaimPeerReviewFactory(BasePeerReviewFactory):
    application_item = factory.SubFactory('factories.policy.EmploymentClaimApplicationItemFactory')
    data = json.dumps({'result': 'verified'})
    result = 'verified'


class RiskAssessmentTaskFactory(factory.DjangoModelFactory):
    user = factory.SubFactory('factories.accounts.UserFactory')
    policy = factory.SubFactory('factories.policy.PolicyApplicationFactory')
    bet1 = 1.5
    bet2 = 2.5

    class Meta:
        model = RiskAssessmentTask
