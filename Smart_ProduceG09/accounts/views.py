from aifc import Error

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def indexPage(request):
    return render(request, 'accounts/index.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            # if user is not None:
            #     login(request, user)
            #     # print(user.username)
            #     return redirect('home')
            # else:
            #     messages.info(request, 'Username OR password is incorrect')

            if user.username == "admin":
                login(request, user)
                # print(user.username)
                return render(request,'accounts/dashboard.html')
            else:
                login(request, user)

                return render(request,'accounts/userOrderPage.html')

        context = {}
        return render(request, 'accounts/login.html', context)

import mysql.connector

import pyqrcode
import png
import shutil
import os

def generateQR(request):

    order_id = request.POST.get('order_id')
    #print(order_id)
    import sqlite3
    request.get_host()
    client_host = request.get_host()
    url = "http:"+str(client_host) + "/order/" + order_id
    print(url)
    # query = '''select id,status from accounts_order where id= %s'''
    # tuple = (order_id, )
    # for p in AccountsOrder.objects.raw(query,tuple):
    #     print((p.status))
    qrcode = pyqrcode.create(url)
    qrcode.png('myqr.png', scale = 6)
    print(os.path.abspath(os.getcwd()))
    shutil.move('myqr.png', 'static/images/icons/myqr2.png')



    # conn = sqlite3.connect('db.sqlite3')
    # conn.execute()
    # mydb = mysql.connector.connect(host="us-cdbr-east-03.cleardb.com", user="b4b07506295099", passwd="90df5ad7")
    # mycursor = mydb.cursor()
    # mycursor.execute("use heroku_cb8e53992ffbeaf")
    # mycursor.execute("select * from patient")
    # patient_list = mycursor.fetchall()
    # print(patient_list)
    # tuple1 = (order_id, )
    # query = ''' SELECT status from accounts_order where id == ? '''
    # cursor = conn.execute(query, tuple1)
    # print(cursor.fetchone())

    # cursor = conn.execute("select * from accounts")
    # print(cursor.fetchall())
    context = {}
    return render(request, 'accounts/generateqr.html', context)

from django.http import HttpResponse

def statusdisplay(request, order_id):
    # print(order_id)
    import sqlite3
    query = '''select id,status from accounts_order where id= %s'''
    tuple = (order_id, )
    for p in AccountsOrder.objects.raw(query, tuple):
        print((p.status))
    # qrcode = pyqrcode.create(p.status)
    # qrcode.png('myqr.png', scale=6)
    # print(os.path.abspath(os.getcwd()))
    # shutil.move('myqr.png', 'static/images/icons/myqr2.png')
    return HttpResponse('<h1>The status of your order {} is {} </h1>'.format(order_id,p.status))

def logoutUser(request):
    logout(request)
    return redirect('index')


def contactPage(request):
    return render(request, 'accounts/Contact.html')


@login_required(login_url='login')
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    Harvested = orders.filter(status='Harvested').count()
    Sorting_center = orders.filter(status='Sorting center').count()
    Quality_check_center = orders.filter(status='quality check center').count()
    out_for_delivery = orders.filter(status='out for delivery').count()

    context = {'orders': orders, 'customers': customers,
               'total_orders': total_orders, 'Harvested': Harvested,
               'Sorting center': Sorting_center, 'quality check center': Quality_check_center,
               'out for delivery': out_for_delivery}

    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer, 'orders': orders, 'order_count': order_count,
               'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'form': formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)
