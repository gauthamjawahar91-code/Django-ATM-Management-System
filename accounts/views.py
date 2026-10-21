from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import Register_form , Login_form , change_pin_Form
from .models import Account
from django.contrib import messages

# Create your views here.
def login(request):
    if request.method == 'POST':
        data_form = Login_form(request.POST)
        if data_form.is_valid():
            acc_no = data_form.cleaned_data['account_no']
            pin_number = data_form.cleaned_data['pin_no']

            user = Account.objects.filter(account_no = acc_no , pin = pin_number).first()

            if user:
                request.session['unique_id'] = user.id
                return redirect('dashboard')
            else:
                messages.error(request ,'Invalid Username or Password')
                return redirect('login')


    loginform = Login_form()
    return render(request,'accounts/login.html',{'login_form':loginform})

    

def logout(request):
    request.session.flush()
    return redirect('login')

def register(request):
    if request.method == 'POST':
        form = Register_form(request.POST)
        if form.is_valid():
            name = form.cleaned_data['Name']
            account_no = form.cleaned_data['Account_no']
            pin = form.cleaned_data['Pin']
            confirm_pin = form.cleaned_data['Confirm_PIn']

            if not(pin==confirm_pin):
                messages.error(request,'Pin and confirm pins are not matching')
                return render(request,'accounts/register.html',{'form':form})

            if Account.objects.filter(account_no=account_no).exists():
                messages.error(request, "Account number already exists.")
                return render(request, "accounts/register.html", {"form": form})

            Account.objects.create(
                name = name,
                account_no = account_no,
                pin = pin,
            )
            messages.success(request,'Account Created Successfully')
            return redirect('login')


    reg_form = Register_form()
    context = {
        'form':reg_form
    }
    return render(request,'accounts/register.html',context)

def change_pin(request):
    if 'unique_id' not in request.session:
        return redirect('login')
    if request.method == "POST":
        new_pin_data = change_pin_Form(request.POST)
        account_details = Account.objects.filter(id = request.session['unique_id']).first()
        if account_details is None:
            messages.error(request,'Account not found')
            return redirect('login')
        if new_pin_data.is_valid():
            old_pin = new_pin_data.cleaned_data['current_pin']
            new_pin = new_pin_data.cleaned_data['new_pin']
            confirm_pin = new_pin_data.cleaned_data['confirm_new_pin']

            if old_pin != account_details.pin:
                messages.error(request,'Current_pin is not matching')
                return render(request,'accounts/change_pin.html',{'change_pin':new_pin_data})
            
            if new_pin != confirm_pin:
                messages.error(request,'new_pin and confirm_pin is not matching')
                return render(request,'accounts/change_pin.html',{'change_pin':new_pin_data})

            if old_pin == new_pin:
                messages.error(request,'old pin cannot be the new pin')
                return render(request,'accounts/change_pin.html',{'change_pin':new_pin_data})
            
            account_details.pin = new_pin
            account_details.save()
            messages.success(request,'Pin Changed Successfully')
            return redirect('dashboard')

            

    changepinform = change_pin_Form()
    context = {
        'change_pin' : changepinform
    }
    return render(request,'accounts/change_pin.html',context)