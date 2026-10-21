from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from .forms import deposit_form , WithdrawForm , TransferForm
from accounts.models import Account
from .models import Transaction
from django.contrib import messages
from django.db import transaction
# Create your views here.

def deposit(request):
    if 'unique_id' not in request.session:
        return redirect('login')
    if request.method == "POST":
        data_form = deposit_form(request.POST)
        if data_form.is_valid():
            amount = data_form.cleaned_data['amount']
            account_id = request.session.get('unique_id')
            account = Account.objects.filter(id = account_id).first()
            account.balance+=amount
            account.save()

            after_balance = account.balance

            messages.success(request,'Amount Deposited Successfully')

            Transaction.objects.create(
                account = account,
                transaction_type = 'DEPOSIT',
                amount = amount,
                balance_after_transaction =  after_balance,
                description = 'Cash Deposited'
            )

            return redirect('dashboard')


    form = deposit_form()
    return render(request,'transactions/deposit.html',{'form':form})

def withdraw(request):
    if 'unique_id' not in request.session:
        return redirect('login')
    if request.method == "POST":
        data_form = WithdrawForm(request.POST)
        if data_form.is_valid():
            amount = data_form.cleaned_data['amount']
            acc_id = request.session['unique_id']
            acc = Account.objects.filter(id=acc_id).first()
            if acc.balance >=amount:
                acc.balance-=amount
                acc.save()

                after_bal = acc.balance

                Transaction.objects.create(
                    account = acc,
                    transaction_type = 'WITHDRAW',
                    amount = amount,
                    balance_after_transaction = after_bal,
                    description = 'Cash Withdrawal'
                )

                messages.success(request,"Please Collect Your Cash")
                return redirect('dashboard')
            else:
                messages.error(request,'Insufficient Balance')
                return render(request,'transactions/withdraw.html',{'form':data_form})


    form = WithdrawForm()
    return render(request,'transactions/withdraw.html',{'form':form})


def transfer(request):
    if 'unique_id' not in request.session:
        return redirect('login')
    if request.method=="POST":
        data_form = TransferForm(request.POST)
        if data_form.is_valid():
            re_acc = data_form.cleaned_data['ReceiverAccountNo']
            amount = data_form.cleaned_data['Amount']

            sender_account = request.session['unique_id']
            sender_details = Account.objects.filter(id = sender_account).first()
            receiver_details = Account.objects.filter(account_no = re_acc).first()

            if not(receiver_details):
                messages.error(request,'Receiver Account Not Found')
                return render(request,'transactions/transfer.html',{'form':data_form})

            if sender_details.account_no == re_acc :
                messages.error(request,'Both Sender and Reciever Account Should not be Same')
                return render(request,'transactions/transfer.html',{'form':data_form})

            if not(sender_details.balance>=amount) :
                messages.error(request,'Insufficient Balance')
                return render(request,'transactions/transfer.html',{'form':data_form})

            with transaction.atomic():

                receiver_details.balance+=amount
                receiver_details.save()

                sender_details.balance-=amount
                sender_details.save()

                after_rec_bal = receiver_details.balance
                after_sen_bal = sender_details.balance

                Transaction.objects.create(
                    account = sender_details,
                    transaction_type = 'TRANSFER_SENT',
                    amount = amount,
                    balance_after_transaction = after_sen_bal,
                    description = f'Money Sent to {re_acc}, ${amount}',
                )

                Transaction.objects.create(
                    account = receiver_details,
                    transaction_type = 'TRANSFER_RECEIVED',
                    amount = amount,
                    balance_after_transaction = after_rec_bal,
                    description = f"{amount} Received from {sender_details.account_no}"
                )

            messages.success(request,'Money Transferred Successfully')
            return redirect('dashboard')



    form = TransferForm()
    return render(request,'transactions/transfer.html',{'form':form})


def mini_statement(request):
    if 'unique_id' not in request.session:
        return redirect('login')

    account_id = request.session['unique_id']

    transactions = Transaction.objects.filter(
        account_id=account_id
    ).order_by('-created_at')[:5]

    return render(request,'transactions/mini_statement.html',
        {'transactions': transactions}
    )


def statement(request):
    if 'unique_id' not in request.session:
        return redirect('login')
    acc = request.session['unique_id']
    trans_details = Transaction.objects.filter(account = acc)
    return render(request,'transactions/statement.html',{'transactions':trans_details})
