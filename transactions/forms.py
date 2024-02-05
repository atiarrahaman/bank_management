from django import forms 
from . models import UserTransactions

class TransactionForm(forms.ModelForm):
    class Meta:
        model = UserTransactions
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.after_transaction = self.account.blance
        return super().save()



class DepositeForm(TransactionForm):
    def clean_amount(self):
        min_amount=100
        max_deposite=100000
        amount=self.cleaned_data.get('amount')
        if amount < min_amount:
            raise forms.ValidationError(f'your deposite {amount} muste be upto {min_amount}')
        
        if amount > max_deposite:
            raise forms.ValidationError(f"you can'nt deposite {amount} .you have permited only lessthan {max_deposite}")
        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.blance # 1000
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance: # amount = 5000, tar balance ache 200
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )

        return amount



class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        return amount
# class UserTransactionsForm(forms.ModelForm):
#     class Meta:
#         model=UserTransactions
#         fields=['amount','transaction_type']
    
#     def __init__(self,*args,**kwargs):
#         self.account=kwargs.pop('account')
#         super().__init__(*args,**kwargs)
#         self.fields['transaction_type'].disable=True
#         self.fields['transaction_type'].widget=forms.HiddenInput()


#     def save(self, commit=True):
#         self.instance.account = self.account
#         self.instance.after_transaction = self.account.blance
#         return super().save()  








# class DepositeForm(UserTransactionsForm):
#     def clean_amount(self):
#         min_amount=100
#         max_deposite=100000
#         amount=self.cleaned_data.get('amount')
#         if amount < min_amount:
#             raise forms.ValidationError(f'your deposite {amount} muste be upto {min_amount}')
        
#         if amount > max_deposite:
#             raise forms.ValidationError(f"you can'nt deposite {amount} .you have permited only lessthan {max_deposite}")
#         return amount


# class WithdrawForm(UserTransactionsForm):
#     def clean_amount(self):
#         account=self.account
#         min_withdraw=100
#         max_withdraw=10000
#         amount=self.cleaned_data.get('amount')
#         blance=account.blance
#         if amount > max_withdraw :
#             raise forms.ValidationError(
#                 f'you can not withdraw up to {max_withdraw} '
#             )
        
#         if amount < min_withdraw:
#             raise forms.ValidationError(
#                 f'must be your withdraw up to {min_withdraw}'
#             )
        
#         if amount > blance :
#             raise forms.ValidationError(
#                 'you have not enough many'
#             )
#         return amount

# class LoanRequestForm(UserTransactionsForm):
#     def clean_amount(self):
#         amount=self.cleaned_data.get('amount')

#         return amount
    


