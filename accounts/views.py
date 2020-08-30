from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group


@unauthenticated_user
def register_page(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + username)
            return redirect('login')
    return render(request, 'accounts/register.html', locals())


@unauthenticated_user
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')
    return render(request, 'accounts/login.html', locals())


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    out_for_deliver_num = Order.objects.filter(status='Out for delivery').count()
    delivered_orders_num = Order.objects.filter(status='Delivered').count()
    pending_orders_num = Order.objects.filter(status='Pending').count()
    return render(request, 'accounts/dashboard.html', locals())


@login_required(login_url='login')
@allowed_users(allowed_rules=['admin'])
def products(request):
    product_list = Product.objects.all()
    return render(request, 'accounts/products.html', locals())


@login_required(login_url='login')
@allowed_users(allowed_rules=['admin'])
def customer(request, customer_id):
    customer_obj = Customer.objects.get(pk=customer_id)
    customer_orders = customer_obj.order_set.all()
    customer_orders_num = customer_orders.count()

    myFilter = OrderFilter(request.GET, queryset=customer_orders)
    customer_orders = myFilter.qs
    return render(request, 'accounts/customer.html', locals())


@login_required(login_url='login')
@allowed_users(allowed_rules=['admin'])
def create_order(request, customer_id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer_obj = Customer.objects.get(pk=customer_id)
    # form = OrderForm(initial={'customer': customer_obj})
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer_obj)
    if request.method == 'GET':
        return render(request, 'accounts/order_form.html', locals())
    elif request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer_obj)
        if formset.is_valid():
            formset.save()
        return redirect('/')


@login_required(login_url='login')
@allowed_users(allowed_rules=['admin'])
def update_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    # get specified order to fill form data
    form = OrderForm(instance=order)
    if request.method == 'GET':
        return render(request, 'accounts/order_form.html', locals())
    elif request.method == 'POST':
        # update current order instance
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
        return redirect('/')


@login_required(login_url='login')
@allowed_users(allowed_rules=['admin'])
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == 'GET':
        return render(request, 'accounts/delete.html', locals())
    elif request.method == 'POST':
        order.delete()
        return redirect('/')


@login_required(login_url='login')
@allowed_users(allowed_rules=['customer'])
def user_page(request):
    orders = request.user.customer.order_set.all()
    out_for_deliver_num = Order.objects.filter(status='Out for delivery').count()
    delivered_orders_num = Order.objects.filter(status='Delivered').count()
    pending_orders_num = Order.objects.filter(status='Pending').count()
    return render(request, 'accounts/user.html')


@login_required(login_url='login')
@allowed_users(allowed_rules=['customer'])
def user_profile(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
    return render(request, 'accounts/profile.html', locals())


