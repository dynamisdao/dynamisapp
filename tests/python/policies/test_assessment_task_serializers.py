from dynamis.apps.policy.api.v1.serializers import RiskAssessmentTaskDetailSerializer, RiskAssessmentTaskShortSerializer


def test_risk_assessment_task_detail_serializer(factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    data = {
        'id': risk_assessment_task.id,
        'policyid': risk_assessment_task.policy.pk,
        'is_finished': risk_assessment_task.is_finished,
        'bet1': risk_assessment_task.bet1,
        'bet2': risk_assessment_task.bet2,
    }

    serializer = RiskAssessmentTaskDetailSerializer(instance=risk_assessment_task)
    assert serializer.data == data


def test_risk_assessment_task_short_serializer(factories):
    risk_assessment_task = factories.RiskAssessmentTaskFactory()

    data = {
        'id': risk_assessment_task.id,
        'is_finished': risk_assessment_task.is_finished,
    }

    serializer = RiskAssessmentTaskShortSerializer(data)
    assert serializer.data == data
