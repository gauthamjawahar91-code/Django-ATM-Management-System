from django.shortcuts import render,redirect
from django.http import HttpResponse
from accounts.models import Account
# Create your views here.
def dashboard(request):
    if 'unique_id' not in request.session:
        return redirect('login')

    account = Account.objects.filter(id = request.session['unique_id']).first()
    if account is None:
        request.session.flush()
        return redirect('login')
    
    context = {
        'account_details' : account 
    }
    return render(request,'dashboard/dashboard.html',context)

def balance(request):
    return HttpResponse("Balance")