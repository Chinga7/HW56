"""online_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from webapp.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, add_to_cart, CartListView, CartDeleteView, OrderCreateView, OrderListView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Product urls
    path('', ProductListView.as_view(), name='product_list'),
    path('product/detail/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),

    # Cart urls
    path('cart/add/<int:pk>/<str:source>/',  add_to_cart, name='cart_add'),
    path('cart/list/',  CartListView.as_view(), name='cart_list'),
    path('cart/delete/<int:pk>/',  CartDeleteView.as_view(), name='cart_delete'),

    # Order urls
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),

]