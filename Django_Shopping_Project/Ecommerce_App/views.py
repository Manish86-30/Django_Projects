from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import customregistration, customlogin
from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import Product, Customer, Cart, OrderPlaced
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



class ProductView(View):
    def get(self, request):
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        topwear = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')

        totalitems = 0
        if request.user.is_authenticated:
            totalitems = Cart.objects.filter(user=request.user).count()
        return render(request, 'app/home.html', {'mobile': mobile, 'laptop': laptop, 'topwear': topwear, 'bottomwear': bottomwear, 'totalitems': totalitems})



class ProductDetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(product=product, user=request.user).exists()


            totalitems = 0
            if request.user.is_authenticated:
                totalitems = Cart.objects.filter(user=request.user).count()
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitems': totalitems})



class MobileView(View):
    def get(self, request, data=None):
        if data == None:
            mobile = Product.objects.filter(category='M')

        elif data == 'Redmi' or data == 'Samsung' or data == 'Apple' or data == 'Xiaomi':
            mobile = Product.objects.filter(category='M').filter(brand=data)

        elif data == 'below':
            mobile = Product.objects.filter(category='M').filter(discounted_price__lt=20000)

        elif data == 'above':
            mobile = Product.objects.filter(category='M').filter(selling_price__gt=20000)
        return render(request, 'app/mobile.html', {'mobile': mobile})


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/registration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successfully')
            return redirect('login')
        return render(request, 'app/registration.html', {'form': form})


'''
class LoginView(View):
    def get(self, request):
        forms = LoginForm()
        return render(request, 'app/login.html', {'forms': forms})

    def post(self, request):
        forms = LoginForm(request.POST)
        if forms.is_valid():
            email = forms.cleaned_data.get('email')
            password = forms.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Login successful')
                return redirect('profile')
            else:
                messages.error(request, 'Invalid email or password')
        return render(request, 'app/login.html', {'forms': forms})
'''

def logoutview(request):
        logout(request)
        return redirect('/')


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()

        totalitems = 0
        if request.user.is_authenticated:
            totalitems = Cart.objects.filter(user=request.user).count()
        return render(request, 'app/profile.html', {'form': form, 'totalitems': totalitems})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile Updated Successfully')
        return render(request, 'app/profile.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class AddressView(View):
    def get(self, request):
        add = Customer.objects.filter(user=request.user)
        return render(request, 'app/address.html', {'address': add})

'''
cart = Cart.objects.create(
    user=request.user,
    product=product  # <- now it's a Product instance
)

user = request.user
        product_id = request.GET.get('pro_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return render(request, 'app/addtocart.html')
'''


class AddtoCartView(View):
    def get(self, request):
        user = request.user
        product_id = request.GET.get('pro_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('showcart')


class ShowCartView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = 0.0
            shipping_amount = 70.0
            total_amount = 0.0
            cart_product = [p for p in Cart.objects.all() if p.user == user]
            if cart_product:
                for p in cart_product:
                    tempamount = (p.quantity * p.product.discounted_price)
                    amount += tempamount
                    totalamount = amount + shipping_amount
                    return render(request, 'app/addtocart.html', {'carts': cart, 'totalamount': totalamount, 'amount': amount})
            else:
                return render(request, 'app/emptycart.html')



def empty(request):
    return render(request, 'app/emptycart.html')



def plus_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.quantity += 1
        cart.save()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
            data = {
                'quantity': cart.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
                }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        try:
            cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        except Cart.DoesNotExist:
            return JsonResponse({"error": "Cart item not found"}, status=404)

        if cart.quantity > 1:
            cart.quantity -= 1
            cart.save()
        else:
            cart.delete()


        amount = 0.0
        shipping_amount = 70.0
        cart_products = Cart.objects.filter(user=request.user)

        for p in cart_products:
            amount += p.quantity * p.product.discounted_price

        data = {
            "amount": amount,
            "totalamount": amount + shipping_amount,
            "quantity": sum(p.quantity for p in cart_products),
        }

        return JsonResponse(data)


def remove_cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        cart = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        cart.delete()

        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            
            
            data = {
                'quantity': cart.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
                }
        return JsonResponse(data)

@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipping_amount
        return render(request, 'app/checkout.html', {'add': add, 'totalamount': totalamount, 'cart_itmes': cart_items})


@method_decorator(login_required, name='dispatch')
class PaymentdoneView(View):
    def get(self, request):
        user = request.user
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
            c.delete()
        return redirect('orders')
    

@method_decorator(login_required, name='dispatch')
class ordersview(View):
    def get(Self, request):
        order = OrderPlaced.objects.filter(user=request.user)
        return render(request, 'app/orders.html', {'orders': order})


def about(request):
    return render(request, 'app/about.html')

def buynow(request):
    return render(request, 'app/buynow.html')
