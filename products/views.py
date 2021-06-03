from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Product, Artist, Label, Genre


def all_products(request):

    products = Product.objects.all()
    a = list(products)

    context = {
        'products': products,
        'a': a
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
