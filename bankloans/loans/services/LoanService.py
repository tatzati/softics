from loans.models import Loan, ProbabilityOfDefault, ExpectedLoss
import requests
import scipy


class LoanService:
    def __init__(self):
            self.loan = None

    @staticmethod
    def retrieve_all_loans():
        return Loan.objects.all()

    def retrieve_loan(self, pk):
        try:
            self.loan = Loan.objects.get(pk=pk)
        except Loan.DoesNotExist:
            self.loan = None

    def check_availability(self):
        if self.loan.saleable == 1:
            return True
        else:
            return False

    def sold(self):
        self.loan.saleable = 0
        self.loan.save()

    def upload_risks(self):
        headers = {'Content-Type': 'application/json'}
        pd = requests.post('http://localhost:5000/api/v1/predict/pd/', headers=headers).json().get('value')
        el = requests.post('http://localhost:5000/api/v1/predict/expected_loss/', headers=headers).json().get('value')
        default = ProbabilityOfDefault(loan=self.loan, risk=pd)
        loss = ExpectedLoss(loan=self.loan, risk=el)
        default.save()
        loss.save()

    def generate_statistics(self):
        pd_list = []
        el_list = []
        pd_set = self.loan.pd_loans.all()
        el_set = self.loan.el_loans.all()
        for pd in pd_set:
            pd_list.append(pd.risk)
        for el in el_set:
            el_list.append(el.risk)
        self.loan.pd_mean = scipy.mean(pd_list)
        self.loan.el_mean = scipy.mean(el_list)
        self.loan.save()

    @staticmethod
    def create_loan(data):
        loan = Loan.objects.create(**data)
        loan_service = LoanService()
        loan_service.retrieve_loan(loan.id)
        loan_service.upload_risks()
        loan_service.generate_statistics()
        return loan

    @staticmethod
    def update_loan(instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.saleable = validated_data.get('saleable', instance.saleable)
        instance.pd_mean = validated_data.get('pd_mean', instance.pd_mean)
        instance.el_mean = validated_data.get('el_mean', instance.el_mean)
        instance.age = validated_data.get('age', instance.age)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        return instance
