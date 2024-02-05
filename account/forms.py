from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import UserAccount,UserAddress
from . constant import ACCCOUNT_TYPE,GENDER




class UserCreateForm(UserCreationForm):
    account_type=forms.ChoiceField(choices=ACCCOUNT_TYPE)
    gender=forms.ChoiceField(choices=GENDER)
    birth_date=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    postal_code=forms.IntegerField()
    streat=forms.CharField( max_length=50)
    city=forms.CharField( max_length=50)
    country=forms.CharField( max_length=50)
    class Meta:
        model=User
        fields=[
            'username','email',
            'password1','password2',
            'first_name','last_name',
            'account_type','gender',
            'birth_date','postal_code',
            'streat',
            'city','country',
            ]
    def save(self,commit=True):
            user_form=super().save(False)
            if commit == True:
                user_form.save()
                account_type=self.cleaned_data.get('account_type')
                gender=self.cleaned_data.get('gender')
                birth_date=self.cleaned_data.get('birth_date')
                postal_code=self.cleaned_data.get('postal_code')
                streat=self.cleaned_data.get('streat')
                city=self.cleaned_data.get('city')
                country=self.cleaned_data.get('country')

                UserAccount.objects.create(
                    user=user_form,
                    account_type=account_type,
                    gender=gender,
                    birth_date=birth_date

                )

                UserAddress.objects.create(
                    user=user_form,
                    postal_code=postal_code,
                    streat=streat,
                    city=city,
                    country=country

                )
            return user_form
            
    def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
        
                for field in self.fields:
                    self.fields[field].widget.attrs.update({
                        
                        'class' : (
                            'appearance-none block w-full bg-gray-200 '
                            'text-gray-700 border border-gray-200 rounded '
                            'py-3 px-4 leading-tight focus:outline-none '
                            'focus:bg-white focus:border-gray-500'
                        ) 
                    })          
