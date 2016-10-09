from dynamis.apps.policy.api.v1.serializers import PolicyListSerializer


def test_policy_list(factories):
    policy = factories.PolicyApplicationFactory()
    data = {'id': policy.pk}

    assert PolicyListSerializer(policy).data == data
