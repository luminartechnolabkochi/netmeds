from django.urls import path
from customers import views


urlpatterns=[
    path("accounts/signup",views.SignUpView.as_view(),name="registration"),
    path("accounts/signin",views.SignInView.as_view(),name="signin"),
    path("index",views.ProductListView.as_view(),name="chome"),
    path("accounts/signout",views.sign_out,name="signout"),
    path("products/all",views.ProductListView.as_view(),name="product-list"),
    path("products/<int:pk>",views.ProductDetailView.as_view(),name="product-detal"),
    path("products/<int:id>/carts/add",views.add_to_cart,name="add-to-cart"),
    path("carts/all",views.MyCartView.as_view(),name="my-cart"),
    path("carts/<int:id>/remove",views.remove_cart_item,name="remove-cart-item"),
    path("orders/<int:cid>/<int:pid>/add",views.PlaceOrderView.as_view(),name="place-order"),
    path("orders/all",views.MyOrdersView.as_view(),name="my-orders"),
    path("order/<int:id>/remove",views.cancel_order,name="remove-order")
]