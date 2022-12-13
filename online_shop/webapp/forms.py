from django import forms
from django.forms import widgets, ValidationError
from webapp.models import Product, Cart, Order

CATEGORY_CHOICES = [
    ('other', 'Other'),
    ('books', 'Books'),
    ('flowers', 'Flowers'),
    ('furniture', 'Furniture'),
    ('gadgets', 'Gadgets')
]


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50, required=False, label="")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['product', 'created_at']


class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        exclude = ['product']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['created_at']

    def leftover_check(self):
        leftover = self.cleaned_data['leftover']
        if leftover < 0:
            self.add_error('leftover', ValidationError('Leftover should be more than zero',
                                                    code='Out of stock', params={'quantity': 0}))
        return leftover

    def price_check(self):
        price = self.cleaned_data['price']
        if price < 0:
            self.add_error('price', ValidationError('Price should be more than zero',
                                                    code='wrong price', params={'quantity': 0}))
        return price