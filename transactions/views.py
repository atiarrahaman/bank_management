from typing import Any


from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView,ListView,View
from . models import UserTransactions
from . forms import DepositeForm,WithdrawForm,LoanRequestForm
from .constant import DEPOSITE,WITHDRAW,LOANREQUEST,LOANPAID
from datetime import datetime
from django.urls import reverse_lazy
from django.db.models import Sum
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Create your views here.
def transaction_email(user,amount,subject,template):
    message=render_to_string(template,{'user':user,'amount':amount})
    send_email=EmailMultiAlternatives(subject,to=[user.email])
    send_email.attach_alternative(message,'text/html')
    send_email.send()
    

class UserTransactionView(LoginRequiredMixin,CreateView):
    template_name='transaction.html'
    model=UserTransactions
    success_url=reverse_lazy('report')
    title='' 


    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.useraccount
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # template e context data pass kora
        context.update({
            'title': self.title
        })

        return context

class DepositeMoneyView(UserTransactionView):
    form_class=DepositeForm
    title='Deposite Money'


    def get_initial(self):
        initial = {'transaction_type':DEPOSITE}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.useraccount
      
        # if not account.initial_deposit_date:
        #     now = timezone.now()
        #     account.initial_deposit_date = now
        account.blance += amount # amount = 200, tar ager balance = 0 taka new balance = 0+200 = 200
        account.save(
            update_fields=[
                'blance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )
        transaction_email(self.request.user,amount,'Deposite success','emailss/depositeemail.html')
        return super().form_valid(form)
    

class WithDrawMoneyView(UserTransactionView):
    form_class=WithdrawForm
    title='Withdraw Money'


    def get_initial(self):
        initial={'transaction_type':WITHDRAW}

        return initial
    

    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        account=self.request.user.useraccount
        
        account.blance -= amount
        account.save(update_fields=['blance'])

        messages.success(
            self.request,
            f'Successfully withdrawn {"{:,.2f}".format(float(amount))}$ from your account'
        )
        transaction_email(self.request.user,amount,'Withdraw Success','emailss/withdrawemail.html')
        return super().form_valid(form)
    

class LoanRequestView(UserTransactionView):
    form_class=LoanRequestForm
    title= 'Loan Request'


    def get_initial(self) :
        initial={'transaction_type':LOANREQUEST}
        return initial
    

    def form_valid(self,form):
        amount=form.cleaned_data.get('amount')
        total_loan_count=UserTransactions.objects.filter(
            account=self.request.user.useraccount,transaction_type=LOANREQUEST,loan_status=True).count()
        if total_loan_count > 3:
            return HttpResponse (f'you have no limite')
        
        messages.success(self.request,f'your loan request{amount}$ success ')
        return super().form_valid(form)
    
   
        
        
    
    




class TransactionReportView(LoginRequiredMixin,ListView):
    template_name='transactionreport.html'
    model=UserTransactions
    balance=0
    ordering=('-id')


    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.useraccount
        )
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            
            queryset = queryset.filter(transactions_date__gte=start_date, transactions_date__lte=end_date)
            self.balance = UserTransactions.objects.filter(
                transactions_date__gte=start_date, transactions_date__lte=end_date
            ).aggregate(Sum('amount'))['amount__sum']
        else:
            self.balance = self.request.user.useraccount.blance
       
        return queryset.distinct() # unique queryset hote hobe
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.useraccount
        })

        return context
    

class LoanPayView(LoginRequiredMixin,View):
    def get(self,request,id):
        loan=get_object_or_404(UserTransactions,id=id)

        if loan.loan_status == True:
            user_account=loan.account

            if loan.amount < user_account.blance:
                user_account.blance -= loan.amount 
                loan.after_transaction = user_account.blance
                user_account.save()
                loan.loan_status=True
                loan.transaction_type=LOANPAID
                loan.save()
                return redirect('report')
            else:
                messages.error(self.request, f'Loan amount is greater than available balance' )


        return redirect('report')
    

class LoanListView(LoginRequiredMixin,ListView):
    template_name='loanlist.html'
    model=UserTransactions
    context_object_name='loan'

    def get_queryset(self):
        user_account=self.request.user.useraccount

        queryset=UserTransactions.objects.filter(account=user_account,transaction_type=LOANREQUEST)
        return queryset







