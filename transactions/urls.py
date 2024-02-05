from django.urls import path 
from .views import DepositeMoneyView,WithDrawMoneyView,LoanRequestView,TransactionReportView,LoanListView,LoanPayView


urlpatterns = [
    path('Deposite/',DepositeMoneyView.as_view(),name='deposite'),
    path('withdraw/',WithDrawMoneyView.as_view(),name='withdraw'),
    path('loanrequest/',LoanRequestView.as_view(),name='loanrequest'),
    path('report/',TransactionReportView.as_view(),name='report'),
    path('loanlist/',LoanListView.as_view(),name='loanlist'),
    path('payloan/<int:id>',LoanPayView.as_view(),name='payloan'),
    
]
