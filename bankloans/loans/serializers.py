from rest_framework import serializers
from .services.BankService import BankService
from .services.LoanService import LoanService
from .services.PDService import PDService
from .services.ELService import ELService
from .models import Loan, Bank


class PDSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True)
    risk = serializers.FloatField(required=False)

    def create(self, validated_data):
        return PDService.create_pd(validated_data)

    def update(self, instance, validated_data):
        return PDService.update_pd(validated_data)


class ELSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField(read_only=True)
    risk = serializers.FloatField(required=False)

    def create(self, validated_data):
        return ELService.create_el(validated_data)

    def update(self, instance, validated_data):
        return ELService.update_el(instance, validated_data)


class LoanSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID', read_only=True)
    title = serializers.CharField(max_length=200, required=False)
    created_at = serializers.DateTimeField(read_only=True)
    bank = serializers.PrimaryKeyRelatedField(read_only=True)
    saleable = serializers.IntegerField(required=False)
    owner = serializers.CharField(required=False)
    pd_mean = serializers.FloatField(required=False)
    el_mean = serializers.FloatField(required=False)
    pd = PDSerializer(many=True, read_only=True, source='pd_loans')
    el = ELSerializer(many=True, read_only=True, source='el_loans')

    def create(self, validated_data):
        return LoanService.create_loan(validated_data)

    def update(self, instance, validated_data):
        return LoanService.update_loan(instance, validated_data)


class BankSerializer(serializers.Serializer):
    id = serializers.UUIDField(format='int')
    name = serializers.CharField(max_length=50, required=False)
    loans = LoanSerializer(many=True, read_only=True)

    def create(self, validated_data):
        return BankService.create_bank(validated_data)

    def update(self, instance, validated_data):
        return BankService.update_bank(instance, validated_data)
