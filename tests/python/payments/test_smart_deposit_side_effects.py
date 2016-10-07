from django.utils import timezone

from dynamis.apps.payments.models import SmartDeposit


def test_check_wait_for_deposit_time(factories):
    user = factories.UserFactory()
    policy = factories.PolicyApplicationFactory(user=user)
    deposit = factories.SmartDepositFactory(policy=policy, state=0)
    assert deposit.wait_for is None
    deposit.init_to_wait()
    deposit = SmartDeposit.objects.get()

    assert deposit.wait_for > timezone.now()
