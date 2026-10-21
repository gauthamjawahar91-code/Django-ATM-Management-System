from django import forms

class deposit_form(forms.Form):
    amount = forms.DecimalField(max_digits=12 , decimal_places=2 , min_value=1)


class WithdrawForm(forms.Form):
    amount = forms.DecimalField(max_digits=12 , decimal_places=2 , min_value=1)

class TransferForm(forms.Form):
    ReceiverAccountNo = forms.IntegerField()
    Amount = forms.DecimalField(max_digits=12 , decimal_places=2 , min_value=1)
