from django.shortcuts import render, redirect
from .models import Good, Contact, Order, OrderUpdate
from math import ceil
import json
from django.contrib.auth.models import User, auth
from django.contrib import messages
import logging
logger = logging.getLogger(__name__)
from django.views.decorators.csrf import csrf_exempt
from .PayTm import Checksum
from django.http import HttpResponse
MERCHANT_KEY = 'Your Merchant Key';

def start(request):
        allIts = []
        catits = Good.objects.values('category', 'id')
        cats = {item['category'] for item in catits}
        for cat in cats:
            prod = Good.objects.filter(category=cat)
            n = len(prod)
            nSlides = n // 4 + ceil((n / 4) - (n // 4))
            allIts.append([prod, range(1, nSlides), nSlides])

        # params = {'no_of_slides':nSlides, 'range': range(1,nSlides),'product': products}
        # allProds = [[products, range(1, nSlides), nSlides],
        #             [products, range(1, nSlides), nSlides]]
        params = {'allIts': allIts}
        return render(request, 'elec/start.html', params)


def goodview(request, myid):
    good = Good.objects.filter(id=myid)
    return render(request, 'elec/goodview.html', {'good': good[0]})

def contact(request):
    if request.method == "POST":
      name = request.POST.get('name', '')
      email = request.POST.get('email', '')
      phone = request.POST.get('phone', '')
      desc = request.POST.get('desc', '')
      contact= Contact(name=name, email=email, phone=phone, desc=desc)
      contact.save()
    return render(request, 'elec/contact.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email taken')
                return redirect('register')
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name, username=username, email=email, password=password1)
                user.save();
                messages.info(request, 'User created')
                return redirect('register')
        else:
            messages.info(request, 'Password not matching...')
            return redirect('register')
    else:
        return render(request, 'elec/register.html')
def login(request):
    if request.method == 'POST':
        username =request.POST['username']
        password =request.POST['password']
        user =auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'elec/login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

def about(request):
    return render(request, 'elec/about.html')


def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        order = Order(items_json=items_json, name=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount=amount)
        order.save()
        thank = True
        id = order.order_id
        param_dict = {
            'MID': '',
            'ORDER_ID': str(order.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/elec/handlerequest/',
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
        return render(request, 'elec/paytm.html', {'param_dict': param_dict})

    return render(request, 'elec/checkout.html')


@csrf_exempt
def handlerequest(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('Order Successful')
        else:
            print('Order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'elec/paymentstatus.html', {'response': response_dict})

def yui(request):
    return render(request, 'elec/yui.html')

def searchMatch(query, item):
    if query in  item.goo_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allIts = []
    catits = Good.objects.values('category', 'id')
    cats = {item['category'] for item in catits}
    for cat in cats:
        prodtemp = Good.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allIts.append([prod, range(1, nSlides), nSlides])
    params = {'allIts': allIts, "msg": ""}
    if len(allIts) == 0 or len(query) < 4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'elec/search.html', params)

