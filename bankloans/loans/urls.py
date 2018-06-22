from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('bank/', views.bank_list),  # List all the banks or create new bank
    path('bank/<int:pk>/', views.bank_details),  # Retrieve bank(pk)
    path('bank/<int:pk>/loans/', views.bank_loans),  # Retrieve or create bank loans
    path('bank/<int:pk>/loans/<int:lpk>/', views.bank_loan_details),  # Update or delete loan(lpk) from bank(pk)
    path('loans/', views.loans_list),  # Get a list of all the loans from all banks
    path('loans/<int:pk>/', views.loan_details),  # Retrieve a loan by pk whatever the bank
    path('loans/<int:pk>/buy/', views.loan_buy),  # Buy loan(pk); Assign owner field to requesting IP
    path('loans/<int:pk>/recalculate/', views.loan_recalculate),  # Recalculate the pd and el for a loan(pk)
]
