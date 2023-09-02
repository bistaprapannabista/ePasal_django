from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from store.models import ProductCategory, Product, Order
from datetime import datetime
from django.views import View
from django.views.generic.detail import DetailView
from store.forms import SignupForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator
# import stripe

# stripe.api_key = "sk_test_4eC39HqLyjWDarjtT1zdp7dc"

def check_user_exists(username):
    user_exists = User.objects.filter(username=username).exists()
    return user_exists


class IndexView(View):
    def get(self, request):
        category_id = request.GET.get('category')
        context = {}
        categories = ProductCategory.objects.filter().order_by('category_name')
        if category_id:
            category_id = int(category_id)
            selected_category = get_object_or_404(
                ProductCategory, id=category_id)
            context["selected_category"] = selected_category
            products = Product.objects.filter(
                product_category=selected_category).order_by('added_on')
        else:
            products = Product.objects.all().order_by('added_on')
        context['category_id'] = category_id
        context['categories'] = categories
        context['products'] = products
        return render(request, "store/index.html", context)

    def post(self,request):
        print(request.POST.get("input"))
        return render(request,"store/index.html",context)

class SearchView(View):
    def get(self,request):
        query = request.GET.get("query")
        result_by_product_name = Product.objects.filter(product_name__icontains=query)
        result_by_product_description = Product.objects.filter(product_description__icontains=query)
        products = result_by_product_description.union(result_by_product_name)
        context = {"products":products,"query":query}
        return render(request,"store/search.html",context)

class LoginView(View):
    form = LoginForm()

    def get(self, request):
        return render(request, "store/login.html", {'form': self.form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is not None:
                login(request, user)
                messages.success(request, "You're logged in successfully.")
                return redirect('/')
            else:
                messages.error(
                    request, "Make sure you enter correct username and password")
                return redirect('/login')


class SignupView(View):
    def get(self, request):
        form = SignupForm()
        return render(request, "store/signup.html", {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():
            if check_user_exists(form.cleaned_data["username"]):
                messages.error(request, "User Already exists.")
                return redirect("/signup")
            elif form.cleaned_data["password1"] != form.cleaned_data["password2"]:
                messages.error(
                    request, "Make Sure both password fields are same.")
                return redirect("/signup")
            else:
                self.create_user(request, form.cleaned_data)
                messages.success(
                    request, "Account created successfully. Login to continue")
                return redirect("/login")
        else:
            messages.error(request, "Form is not valid.")

        return redirect("/signup")

    def create_user(self, request, cleaned_data):
        user = User.objects.create_user(
            username=cleaned_data["username"], password=cleaned_data["password1"], email=cleaned_data["email"])
        user.first_name = cleaned_data["firstname"]
        user.last_name = cleaned_data["lastname"]
        user.save()


class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product-detail.html"

    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        cart = request.session.get('cart')
        if cart:
            if request.POST.get('remove') == "true":
                cart[product_id] = cart[product_id]-1
            else:
                quantity = cart.get(product_id)
                if quantity:
                    cart[product_id] = quantity+1
                else:
                    cart[product_id] = 1
        else:
            cart = {}
            cart[product_id] = 1
        request.session['cart'] = cart
        return redirect(f"/product/{product_id}")

class CartView(View):
    def get(self,request):
        if not request.session.get('cart'):
            messages.success(request, "Your cart is empty please add atleast one product to your cart.")
            return redirect("/")
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        return render(request,'store/cart.html',{'products':products})


class CheckoutView(View):
    @method_decorator(auth_middleware)
    def post(self,request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        user = User.objects.get(id=request.user.id)
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        
        for product in products:
            order = Order(user=user,
            product=Product.get_product(product.id),
            price = product.product_price,
            address = address,
            phone = phone,
            quantity = cart.get(str(product.id)))
            order.placeOrder()
        del request.session['cart']

        # stripe.PaymentIntent.create(
        # amount=500,
        # currency="gbp",
        # payment_method="pm_card_visa",
        # )
        return redirect('/orders')


class OrderView(View):
    @method_decorator(auth_middleware)
    def get(self,request):
        orders = Order.get_orders_by_user(request.user.id)
        return render(request,'store/orders.html',{'orders':orders})




