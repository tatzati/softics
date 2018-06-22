from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LoanSerializer, BankSerializer
from .services.LoanService import LoanService
from .services.BankService import BankService
from .models import Loan, Bank


@api_view(['GET', 'POST'])
def bank_list(request):
    """
    List all the banks or create new bank
    :param request:
    :return Bank serialized data:
    """
    if request.method == 'GET':
        banks = BankService().retrieve_all_banks()
        serializer = BankSerializer(banks, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BankSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def bank_details(request, pk):
    """
    Retrieve bank(pk)
    :param request:
    :param pk:
    :return:
    """
    bank_service = BankService()
    if bank_service.retrieve_bank(pk):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BankSerializer(bank_service.bank)
        return Response(serializer.data)


@api_view(['GET', 'POST'])
def bank_loans(request, pk):
    """
    Retrieve or create bank loans
    :param request:
    :param pk:
    :return Bank serialized data:
    """
    bank_service = BankService()
    if bank_service.retrieve_bank(pk):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BankSerializer(bank_service.bank)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = LoanSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(bank=bank_service.bank)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'DELETE'])
def bank_loan_details(request, pk, lpk):
    """
    Update or delete loan(lpk) from bank(pk)
    :param request:
    :param pk:
    :param lpk:
    :return:
    """
    bank_service = BankService()
    if bank_service.retrieve_bank(pk):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        loan = bank_service.bank.loans.get(pk=lpk)
        serializer = LoanSerializer(loan, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    elif request.method == 'DELETE':
        loan = bank_service.bank.loans.get(pk=lpk)
        loan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def loans_list(request):
    """
    Get a list of all the loans from all banks
    :param request:
    :return All loans serialized data:
    """
    if request.method == 'GET':
        loans = LoanService().retrieve_all_loans()
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def loan_details(request, pk):
    """
    Retrieve a loan by pk whatever the bank
    :param request:
    :param pk:
    :return Loan(pk) serialized data:
    """
    loan_service = LoanService()
    if loan_service.retrieve_loan(pk):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        loan_service.upload_risks()
        loan_service.generate_statistics()
        serializer = LoanSerializer(loan_service.loan)
        return Response(serializer.data)


@api_view(['POST'])
def loan_buy(request, pk):
    """
    Buy loan(pk); Assign owner field to requesting name, mark as sold; saleable = 0
    :param request:
    :param pk:
    :return Loan(pk) serialized data:
    """
    loan_service = LoanService()
    if loan_service.retrieve_loan(pk):
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if not loan_service.check_availability():
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
        loan_service.sold()
        serializer = LoanSerializer(loan_service.loan, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def loan_recalculate(request, pk):
    """
    Recalculate the probability of default and expected loss for a loan(pk)
    :param request:
    :param pk:
    :return list of dictionaries containing {date: date, value: risk} for pd and el risk values:
    """
    if request.method == 'GET':
        loan_service = LoanService()
        if loan_service.retrieve_loan(pk):
            return Response(status=status.HTTP_404_NOT_FOUND)
        loan_service.upload_risks()
        loan_service.generate_statistics()
        serializer = LoanSerializer(loan_service.loan)
        return Response(serializer.data)
