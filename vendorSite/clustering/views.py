from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

from . models import CustomerBill

# Create your views here.


def addBilling(request):
    if request.method == 'POST':
        phoneNumber = request.POST['phoneNumber']
        billAmount = request.POST['billAmount']
        annualIncome = request.POST['annualIncome']

        # Calculate Spending Score
        temp = (int(annualIncome)/40)
        spendingScore = ((int(billAmount)/int(temp))*100) % 100

        if CustomerBill.objects.filter(vendor=request.user, phoneNumber=phoneNumber).exists():
            customer = CustomerBill.objects.filter(
                vendor=request.user, phoneNumber=phoneNumber).first()
            # Calculate Spending Score
            temp = (int(annualIncome)/40)
            spendingScore = ((int(billAmount)/int(temp))*100) % 100
            customer.spendingScore = (
                int(customer.spendingScore) + int(spendingScore))/2
            customer.annualIncome = annualIncome
            customer.save()
        else:
            customer = CustomerBill.objects.create(
                vendor=request.user, phoneNumber=phoneNumber, spendingScore=spendingScore, annualIncome=annualIncome)
            customer.save()
        messages.info(request, 'Record Added!')
        return redirect('/')
    else:
        return render(request, '/')


def customerDatabase(request):
    customerDataList = CustomerBill.objects.filter(
        vendor=request.user)
    temp = []
    for i in customerDataList:
        temp.append(i)

    context = {
        'customerData': temp,
    }
    return render(request, 'database.html', context)
