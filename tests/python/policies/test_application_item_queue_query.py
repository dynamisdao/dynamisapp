import pytest


@pytest.fixture
def application_items(factories):
    other_user_a = factories.UserFactory()
    other_user_b = factories.UserFactory()

    policy_a = factories.PolicyApplicationFactory(user=other_user_a)
    policy_b = factories.PolicyApplicationFactory(user=other_user_b)

    item_a_1 = factories.IdentityApplicationItemFactory(policy_application=policy_a)
    item_a_2 = factories.IdentityApplicationItemFactory(policy_application=policy_a)

    item_b_1 = factories.IdentityApplicationItemFactory(policy_application=policy_b)
    item_b_2 = factories.IdentityApplicationItemFactory(policy_application=policy_b)
    item_b_3 = factories.IdentityApplicationItemFactory(policy_application=policy_b)

    return (
        (other_user_a, (policy_a, (item_a_1, item_a_2))),
        (other_user_b, (policy_b, (item_b_1, item_b_2, item_b_3))),
    )


def assert_qs_equal(left, right):
    left_pks = {v.pk for v in left}
    right_pks = {v.pk for v in right}

    assert left_pks == right_pks


def test_application_item_queue_with_no_peer_reviews(application_items, user,
                                                     models):
    other_user_a = application_items[0][0]
    item_a_1, item_a_2 = application_items[0][1][1]

    other_user_b = application_items[1][0]
    item_b_1, item_b_2, item_b_3 = application_items[1][1][1]

    base_user_queue = models.ApplicationItem.objects.get_review_queue(user)
    user_a_queue = models.ApplicationItem.objects.get_review_queue(other_user_a)
    user_b_queue = models.ApplicationItem.objects.get_review_queue(other_user_b)

    assert_qs_equal(
        (item_a_1, item_a_2, item_b_1, item_b_2, item_b_3),
        base_user_queue,
    )
    assert_qs_equal(
        (item_b_1, item_b_2, item_b_3),
        user_a_queue
    )
    assert_qs_equal(
        (item_a_1, item_a_2),
        user_b_queue
    )


def test_application_item_queue_with_reviewed_items(application_items,
                                                    user, models,
                                                    factories):
    item_a_1, item_a_2 = application_items[0][1][1]

    item_b_1, item_b_2, item_b_3 = application_items[1][1][1]

    # Lets create an un-finalized
    factories.IdentityPeerReviewFactory(
        application_item=item_a_2, user=user,
    )
    factories.IdentityPeerReviewFactory(
        application_item=item_b_3, user=user,
    )

    base_user_queue = models.ApplicationItem.objects.get_review_queue(user)

    assert_qs_equal(
        (item_a_1, item_b_1, item_b_2),
        base_user_queue,
    )
