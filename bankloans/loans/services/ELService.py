from loans.models import ExpectedLoss


class ELService:

    @staticmethod
    def create_el(data):
        return ExpectedLoss.objects.create(**data)

    @staticmethod
    def update_el(instance, validated_data):
        instance.risk = validated_data.get('risk', instance.risk)
        instance.save()
        return instance
