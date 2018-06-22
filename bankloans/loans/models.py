from django.db import models


class Bank(models.Model):
    name = models.CharField(max_length=50, default='bank')

    objects = models.Manager()

    def __str__(self):
        return self.name


class Loan(models.Model):
    title = models.CharField(max_length=200, default='loan')
    created_at = models.DateTimeField(auto_now_add=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="loans")
    pd_mean = models.FloatField(default=0.0)
    el_mean = models.FloatField(default=0.0)
    age = models.IntegerField(default=0)
    amount = models.IntegerField(default=0)
    owner = models.CharField(max_length=200, default='0.0.0.0')
    saleable = models.IntegerField(default=1)

    objects = models.Manager()

    def __str__(self):
        return self.title


class ProbabilityOfDefault(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="pd_loans", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    risk = models.FloatField(default=0.00)

    objects = models.Manager()


class ExpectedLoss(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="el_loans", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    risk = models.FloatField(default=0.00)

    objects = models.Manager()
