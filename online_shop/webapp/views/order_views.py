from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import ListView, View
from webapp.forms import OrderForm
from webapp.models import Order, Cart, ProductOrder


class OrderListView(ListView):
    template_name = 'order/list.html'
    model = Order
    context_object_name = 'orders'


class OrderCreateView(View):
    def post(self, request, *args, **kwargs):
        form = OrderForm(data=request.POST)
        cart_items = Cart.objects.all()
        if form.is_valid() and cart_items:
            for item in cart_items:
                order = Order.objects.create(**form.cleaned_data)
                order.product.pk = item.product.pk
                ProductOrder.objects.create(order_id=order.pk, product_id=item.product.pk, quantity=item.quantity)
            cart_items.delete()
            return redirect('order_list')
        elif form.is_valid():
            return render(request, 'cart/list.html', {'form': form})
        else:
            return render(request, 'cart/list.html')
        