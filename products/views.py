from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.contrib.auth.models import User

from .models import Product, Genre, ProductReview
from wishlist.models import Wishlist
from .forms import ProductForm, ProductReviewForm


def all_products(request):

    products = Product.objects.all()
    query = None
    genres = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'artist':
                sortkey = 'lower_artist'
                products = products.annotate(lower_artist=Lower('artist'))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'genre' in request.GET:
            genres = request.GET['genre'].split(',')
            products = products.filter(genre__name__in=genres)
            genres = Genre.objects.filter(name__in=genres)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(artist__icontains=query) | Q(title__icontains=query) | Q(genre__name__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_genres': genres,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    reviews = ProductReview.objects.filter(product=product)
    try:
        wishlist = get_object_or_404(Wishlist, user=request.user.id)
        if product in wishlist.products.all():
            in_wishlist = True
        else:
            in_wishlist = False
    except Exception:
        in_wishlist = False

    if request.user.is_authenticated:
        already_reviewed = ProductReview.objects.filter(user=request.user)
    else:
        already_reviewed = False

    review_form = ProductReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'already_reviewed': already_reviewed,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def edit_product(request, product_id):
    """ A view to edit individual product details """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)    
    if request.method == 'POST':
        current_title = product.title
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            current_sku = request.POST['sku']            
            sku_exists = Product.objects.filter(
                sku=current_sku).exclude(title=current_title)
            print(current_title)
            if sku_exists:
                messages.error(request,
                               'Another title with that SKU already exists!')
            else:
                form.save()
                messages.info(request, 'Successfully updated product!')
                return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure \
                           the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.title}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def add_product(request):
    """ A view to add individual product details """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_sku = request.POST['sku']
            sku_exists = Product.objects.filter(sku=new_sku)
            if sku_exists:
                messages.error(request, 'That SKU already exists!')
            else:
                product = form.save()
                messages.info(request, 'Successfully added product!')
                return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the \
                           form is valid.')
    else:
        form = ProductForm()
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ A view to delete individual product details """

    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)

    product.delete()
    messages.info(request, 'Product deleted!')
    return redirect(reverse('products'))


@login_required
def add_product_review(request, product_id):
    """ A view to add a product review
    """
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        review_form = ProductReviewForm(request.POST)

        if review_form.is_valid():
            ProductReview.objects.create(
                product=product,
                user=request.user,
                body=request.POST['body'],
                review_rating=request.POST['review_rating'],
            )

            messages.info(request, 'Successfully added a review!')
            return redirect(reverse('product_detail', args=[product.id]))


@login_required
def edit_product_review(request, product_id, review_author):
    """ A view to edit a product review
    """
    product = get_object_or_404(Product, pk=product_id)
    review = ProductReview.objects.filter(product=product, user__username=review_author)[0]  ################

    if request.user != review.user and not request.user.is_superuser:
        messages.error(request, "Sorry, you don't have permission to do that.")
        return redirect(reverse('home'))

    if request.method == 'POST':
        review_form = ProductReviewForm(request.POST)
        if review_form.is_valid():
            review.body = request.POST['body']
            review.review_rating = request.POST['review_rating']
            if 'admin_comment' in request.POST:
                review.admin_comment = request.POST['admin_comment']
            review.save()
            messages.info(request, 'Review Updated!')
            return redirect(reverse('product_detail', args=[product.id]))
    else:
        review_form = ProductReviewForm(initial={
            'body': review.body,
            'review_rating': review.review_rating,
            'admin_comment': review.admin_comment,
        })

    template = 'products/edit_product_review.html'
    context = {
        'review': review,
        'review_form': review_form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def delete_product_review(request, product_id, review_author):
    """ A view to delete a product review """
    product = get_object_or_404(Product, pk=product_id)
    review = ProductReview.objects.filter(product=product, user__username=review_author)[0] ################

    if request.user != review.user and not request.user.is_superuser:
        messages.error(request, "Sorry, you don't have permission to do that.")
        return redirect(reverse('home'))

    review.delete()
    messages.info(request, 'Review deleted!')
    return redirect(reverse('product_detail', args=[product.id]))


@login_required
def upvote_product_review(request, product_id, review_author):
    """ A view to edit a product review
    """
    product = get_object_or_404(Product, pk=product_id)
    review = ProductReview.objects.filter(product=product, user__username=review_author)[0] ################

    if not review:
        messages.error(request, "Sorry, you don't have permission to do that.")
        return redirect(reverse('home'))

    if not review.upvote_list.filter(id=request.user.id):
        review.upvote_list.add(request.user)
        review.upvote_count = review.upvote_list.all().count()
        review.save()
        messages.info(request, 'Liked Review!')
        return redirect(reverse('product_detail', args=[product.id]))
    messages.info(request, 'Already Liked!')
    return redirect(reverse('product_detail', args=[product.id]))