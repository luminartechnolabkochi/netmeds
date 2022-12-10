from django.shortcuts import render,redirect
from customers import forms
from django.views.generic import CreateView,View,FormView,TemplateView,ListView,DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from crm.models import Product,Cart,Order
# Create your views here.



class SignUpView(CreateView):

    template_name="customers/signup.html"
    form_class=forms.UserRegistrationForm
    success_url=reverse_lazy("signin")

    def form_valid(self, form):
        messages.success(self.request,"your account has been created successfuly")

        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"registration failed")
        return super().form_invalid(form)

class SignInView(FormView):
    template_name="customers/signin.html"
    form_class=forms.LoginForm
    def post(self,request,*args,**kw):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            password=form.cleaned_data.get("password")
            user=authenticate(request,username=username,password=password)
            if user:
                login(request,user)
                messages.success(request,"you are signed in now")
                if request.user.is_superuser:
                    return redirect("home")
                else:
                    return redirect("chome")
            else:
                messages.error(request,"invalid credentials")
                return render(request,self.template_name,{"form":form})

class IndexView(TemplateView):
    template_name="customers/index.html"



def sign_out(request,*args,**kw):
    logout(request)
    return redirect("signin")

class ProductListView(ListView):
    template_name="customers/product-list.html"
    model=Product
    context_object_name="products"



class ProductDetailView(DetailView):
    template_name="customers/product-details.html"
    model=Product
    context_object_name="product"


def add_to_cart(request,*args,**kw):
    id=kw.get("id")
    product=Product.objects.get(id=id)
    Cart.objects.create(user=request.user,
    product=product)
    messages.success(request,"item has been added to cart")
    return redirect("chome")

class MyCartView(TemplateView):
    template_name="customers/cart-items.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        items=Cart.objects.filter(user=self.request.user)
        context["products"]=items
        return context


def remove_cart_item(request,*args,**kw):
    id=kw.get("id")
    Cart.objects.filter(id=id).delete()
    messages.success(request,"item has been removed from cart")
    return redirect("chome")

class PlaceOrderView(TemplateView):
    template_name="customers/place-order.html"
    
    def get(self,request,*args,**kw):
        cid=kw.get("cid")
        pid=kw.get("pid")
        product=Product.objects.get(id=pid)
        return render(request,self.template_name,{"product":product})
    def post(self,request,*args,**kw):
        cid=kw.get("cid")
        pid=kw.get("pid")
        product=Product.objects.get(id=pid)
        cart=Cart.objects.get(id=cid)
        address=request.POST.get("address")
        Order.objects.create(customer=request.user,
                            product=product,
                            delivery_address=address

            )
        cart.status="ORDER-PLACED"
        cart.save()
        messages.success(request,"your order hasbeen placed successfully")
            
        return redirect("chome")
class MyOrdersView(ListView):
    template_name="customers/orders.html"
    model=Order
    context_object_name="orders"

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user).order_by("-date_created")


def cancel_order(request,*args,**kw):
    id=kw.get("id")
    Order.objects.filter(id=id).delete()
    messages.success(request,"your order has been cancelled")
    return redirect("chome")
