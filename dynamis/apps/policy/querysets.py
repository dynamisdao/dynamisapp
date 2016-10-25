from django.db import models


class ApplicationItemQueryset(models.QuerySet):
    def get_review_queue(self, user):
        return self.exclude(
            # no items that are from your own application.
            policy_application__user=user,
        ).exclude(
            # no items that you have already reviewed
            peer_reviews__user=user,
        ).exclude(is_finished=True)
