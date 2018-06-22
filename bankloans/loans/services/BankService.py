from loans.models import Bank


class BankService:
    def __init__(self):
        self.bank = None

    def retrieve_bank(self, pk):
        try:
            self.bank = Bank.objects.get(pk=pk)
        except Bank.DoesNotExist:
            self.bank = None

    @staticmethod
    def retrieve_all_banks():
        return Bank.objects.all()

    @staticmethod
    def create_bank(data):
        return Bank.objects.create(**data)

    @staticmethod
    def update_bank(instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
