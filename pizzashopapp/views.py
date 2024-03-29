from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from pizzashopapp.forms import UserForm, PizzaShopForm, UserFormForEdit, PizzaForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from pizzashopapp.models import Pizza


# Create your views here.
def home(request):
    return redirect('pizzapp:pizzashop-home')

# @login_required(login_url='pizzapp:pizzashop-sign-in')
def pizzashop_home(request):
    if not hasattr(request.user, 'pizzashop'):
        request = auto_login(request)
    return redirect('pizzapp:pizzashop-pizza')


@login_required(login_url='pizzapp:pizzashop-sign-in')
def pizzashop_account(request):
    user_form = UserFormForEdit(instance=request.user)
    pizzashop_form = PizzaShopForm(instance=request.user.pizzashop)

    if request.method == "POST":
        user_form = UserFormForEdit(request.POST, instance=request.user)
        pizzashop_form = PizzaShopForm(request.POST, request.FILES, instance=request.user.pizzashop)

        if user_form.is_valid() and pizzashop_form.is_valid():
            user_form.save()
            pizzashop_form.save()

    return render(request, 'pizzashop/account.html', {
        'user_form': user_form,
        'pizzashop_form': pizzashop_form
    })


# @login_required(login_url='pizzapp:pizzashop-sign-in')
def pizzashop_pizza(request):
    if not hasattr(request.user, 'pizzashop'):
        request = auto_login(request)
    try:
        pizzas = Pizza.objects.filter(pizzashop=request.user.pizzashop).order_by("-id")
    except:
        return redirect('pizzapp:pizzashop-sign-in')
    return render(request, 'pizzashop/pizza.html', {
        'pizzas': pizzas
    })


@login_required(login_url='pizzapp:pizzashop-sign-in')
def pizzashop_add_pizza(request):
    form = PizzaForm()
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES)
        if form.is_valid():
            pizza = form.save(commit=False)
            pizza.pizzashop = request.user.pizzashop
            pizza.save()
            return redirect('pizzapp:pizzashop-pizza')

    return render(request, 'pizzashop/add_pizza.html', {
        'form': form
    })


@login_required(login_url='pizzapp:pizzashop-sign-in')
def pizzashop_edit_pizza(request, pizza_id):
    form = PizzaForm(instance = Pizza.objects.get(id = pizza_id))
    if request.method == "POST":
        form = PizzaForm(request.POST, request.FILES, instance = Pizza.objects.get(id = pizza_id))
        if form.is_valid():
            pizza = form.save()
            return redirect('pizzapp:pizzashop-pizza')

    return render(request, 'pizzashop/edit_pizza.html', {
        'form': form
    })


def pizzashop_sign_up(request):
    user_form = UserForm()
    pizzashop_form = PizzaShopForm()

    if request.method == "POST":
        user_form = UserForm(request.POST)
        pizzashop_form = PizzaShopForm(request.POST, request.FILES)

        if user_form.is_valid() and pizzashop_form.is_valid():
            new_user = User.objects.create_user(**user_form.cleaned_data)
            new_pizzashop = pizzashop_form.save(commit=False)
            new_pizzashop.owner = new_user
            new_pizzashop.save()

            login(request, authenticate(
                username = user_form.cleaned_data['username'],
                password = user_form.cleaned_data['password']
            ))

            return redirect('pizzapp:pizzashop-home')

    return render(request, 'pizzashop/sign_up.html', {
        'user_form': user_form,
        'pizzashop_form': pizzashop_form
    })


def auto_login(request):
    # Auto-login with test user Vanya:
    vanya = get_object_or_404(User, username='Vanya')
    if vanya:
        request.user = authenticate(username='Vanya', password='1234')
        login(request, request.user)
    return request
