from django import forms 

class Register_form(forms.Form):
    Name = forms.CharField()
    Account_no = forms.IntegerField()
    Pin = forms.CharField(max_length=4)
    Confirm_PIn = forms.CharField(max_length=4)

class Login_form(forms.Form):
    account_no = forms.IntegerField()
    pin_no = forms.CharField(widget=forms.PasswordInput())

class change_pin_Form(forms.Form):
    current_pin = forms.CharField(widget=forms.PasswordInput())
    new_pin = forms.CharField(widget=forms.PasswordInput(),max_length=4)
    confirm_new_pin = forms.CharField(widget=forms.PasswordInput(),max_length=4)