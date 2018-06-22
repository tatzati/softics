from loans.models import ProbabilityOfDefault


class PDService:

    @staticmethod
    def create_pd(data):
        return ProbabilityOfDefault.objects.create(**data)

    @staticmethod
    def update_pd(instance, validated_data):
        instance.risk = validated_data.get('risk', instance.risk)
        instance.save()
        return instance