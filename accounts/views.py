from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *  
from .forms import OrderForm,CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
#from .decorators import unauthenticated_user, allowed_users, admin_only
# Create your views here.
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        # print(form)
        if form.is_valid():
            # print("Enter")
            user = form.save()
            username = form.cleaned_data.get('username')

            # group = Group.objects.get(name='customer')
            # user.groups.add(group)
            # Customer.objects.create(
            #     user=user,
            #     name=user.username,
            # )

            messages.success(request, 'Account was created for '+ username)
            return redirect("login")
            
    context = {'form':form}
    return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    else:
        if request.method == 'POST':

            username = request.POST.get('username')
            password = request.POST.get('password')

            user=auth.authenticate(username=username, password=password)


        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
            # return render(request, 'accounts/login.html')
        context = {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    out_for_deliery = orders.filter(status='Out for delivery').count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,
        'out_for_deliery':out_for_deliery,
    }
    return render(request, 'accounts/dashboard.html', context)
@login_required(login_url='login')
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer':customer, 
        'orders':orders, 
        'order_count':order_count,
        'myFilter':myFilter,
    }
    return render(request, 'accounts/customer.html', context)

def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products':products})
@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    #print('CUSTOMER ',customer)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    #form = OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        # print('Pricing Post: ', request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    print('ORDER:', order)

    if request.method == 'POST':
        # print('Pricing Post:', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect("/")
    context = {'item':order}
    return render(request, 'accounts/delete.html', context)



