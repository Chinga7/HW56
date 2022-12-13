from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from webapp.models import Cart, Product
from webapp.forms import OrderForm


class CartListView(ListView):
    template_name = 'cart/list.html'
    model = Cart
    context_object_name = 'items'
    total = 0

    def get_queryset(self):
        queryset = super().get_queryset()
        if queryset:
            response = []
            for item in queryset:
                sum = item.quantity * item.product.price
                response.append({
                    'pk': item.pk,
                    'name': item.product.name,
                    'price': item.product.price,
                    'quantity': item.quantity,
                    'sum': sum
                })
                self.total += sum
            queryset = response
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['total'] = self.total
        context['form'] = OrderForm
        return context


class CartDeleteView(DeleteView):
    template_name = 'cart/delete.html'
    model = Cart
    context_object_name = 'cart'
    success_url = reverse_lazy('cart_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.product.leftover += self.object.quantity
        self.object.product.save()
        self.object.delete()
        return HttpResponseRedirect(success_url)


def add_to_cart(request, pk, source):
    product = get_object_or_404(Product, pk=pk)
    cart = Cart.objects.filter(product_id=pk).first()
    if cart and product.leftover > 0:
        cart.quantity += 1
        product.leftover -= 1
        product.save()
        cart.save()
    elif not cart and product.leftover > 0:
        Cart.objects.create(product_id=pk, quantity=1)
        product.leftover -= 1
        product.save()
    if source=='detail':
        return redirect('product_detail', pk)
    return redirect('product_list')