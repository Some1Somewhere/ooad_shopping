from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
from django.contrib import messages
from .models import Product, Order
from .forms import CartForm, CheckoutForm
from . import cart

# Create your views here.


def index(request):
    if request.method == 'GET':
        query= request.GET.get('q')
        if query is not None:
            lookups= Q(name__icontains=query) | Q(description__icontains=query)
            results= Product.objects.filter(lookups).distinct()
            return render(request, "ecommerce_app/index.html", {
                                    'all_products': results,
                                    })
    all_products = Product.objects.all().order_by('-clicks')
    return render(request, "ecommerce_app/index.html", {
                                    'all_products': all_products,
                                    })


def show_product(request, product_id, product_slug):
    product = get_object_or_404(Product, id=product_id)
    product.clicks += 1
    print("Clicks updated")
    product.save()

    if request.method == 'POST':
        form = CartForm(request, request.POST)
        if form.is_valid():
            request.form_data = form.cleaned_data
            cart.add_item_to_cart(request)
            return redirect('show_cart')

    form = CartForm(request, initial={'product_id': product.id})
    return render(request, 'ecommerce_app/product_detail.html', {
                                            'product': product,
                                            'form': form,
                                            })


def show_cart(request):

    if request.method == 'POST':
        if request.POST.get('submit') == 'Update':
            cart.update_item(request)
        if request.POST.get('submit') == 'Remove':
            cart.remove_item(request)

    cart_items = cart.get_all_cart_items(request)
    cart_subtotal = cart.subtotal(request)
    return render(request, 'ecommerce_app/cart.html', {
                                            'cart_items': cart_items,
                                            'cart_subtotal': cart_subtotal,
                                            })


def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            o = Order(
                name = cleaned_data.get('name'),
                email = cleaned_data.get('email'),
                postal_code = cleaned_data.get('postal_code'),
                address = cleaned_data.get('address'),
            )
            o.save()

            all_items = cart.get_all_cart_items(request)
            
            cart.clear(request)

            request.session['order_id'] = o.id

            messages.add_message(request, messages.INFO, 'Order Placed!')
            return redirect('checkout')


    else:
        form = CheckoutForm()
        return render(request, 'ecommerce_app/checkout.html', {'form': form})

