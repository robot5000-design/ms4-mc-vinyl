from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse)
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower
from django.http import Http404

from wishlist.models import Wishlist
from .models import Product, Genre, ProductReview, Promotion
from .forms import ProductForm, ProductReviewForm, GenreForm, PromotionForm


def all_products(request):
    """ Gets, sorts and searches all products in the database for
    the products page.

    Args:
        request (object): HTTP request object.
    Returns:
        Render of the products template.
        Redirects to products url after a search.
    """
    products = Product.objects.all()
    query = None
    genres = None
    promotions = None
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
            if sortkey == 'rating' or sortkey == '-rating':
                products = products.order_by(sortkey).exclude(rating=None)
            else:
                products = products.order_by(sortkey)

        if 'genre' in request.GET:
            genres = request.GET['genre'].split(',')
            products = products.filter(genre__name__in=genres)
            genres = Genre.objects.filter(name__in=genres).order_by('name')

        if 'promotion' in request.GET:
            promotions = request.GET['promotion'].split(',')
            products = products.filter(promotion__name__in=promotions)
            promotions = Promotion.objects.filter(
                name__in=promotions).order_by('name')

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(
                    request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            queries = (
                Q(artist__icontains=query) |
                Q(title__icontains=query) |
                Q(genre__name__icontains=query)
            )
            products = products.filter(queries).distinct()

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_genres': genres,
        'current_sorting': current_sorting,
        'current_promotions': promotions,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details including product reviews.

    Args:
        request (object): HTTP request object.
        product_id (int): id which identifies a product in the database.
    Returns:
        Render of the product_details template.
    """
    product = get_object_or_404(Product, pk=product_id)
    reviews = ProductReview.objects.filter(product=product)
    current_sorting = 'date_desc'

    if 'sort' in request.GET:
        sortkey = request.GET['sort']
        sort = sortkey
        if sortkey == 'date':
            sortkey = 'review_date'
        if sortkey == 'likes':
            sortkey = 'upvote_count'
        if sortkey == 'rating':
            sortkey = 'review_rating'
        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                sortkey = f'-{sortkey}'
        reviews = reviews.order_by(sortkey)
        current_sorting = f'{sort}_{direction}'

    try:
        wishlist = get_object_or_404(Wishlist, user=request.user.id)
    except Http404:
        in_wishlist = False
    else:
        in_wishlist = bool(product in wishlist.products.all())

    if request.user.is_authenticated:
        already_reviewed = ProductReview.objects.filter(product=product,
                                                        user=request.user)
    else:
        already_reviewed = False

    review_form = ProductReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'already_reviewed': already_reviewed,
        'in_wishlist': in_wishlist,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def edit_product(request, product_id):
    """ A view to edit individual product details.

    Gets a products details from the database for editing. If the sku
    is changed to one that already exists the user is warned.

    Args:
        request (object): HTTP request object.
        product_id (int): id which identifies a product in the database.
    Returns:
        Render of the edit_product template.
        Redirects to home url if not superuser.
        Redirects to product_detail page upon successful or failed update.
    """
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
        messages.info(request, 'You are editing a product.')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def add_product(request):
    """ A view to add individual product details.

    The user is warned if the sku chosen already exists in the database.

    Args:
        request (object): HTTP request object.
    Returns:
        Render of the add_product template.
        Redirects to home url if not superuser.
        Redirects to product_detail page upon successful or failed update.
    """
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
    """ A view to delete individual product details.

    Args:
        request (object): HTTP request object.
        product_id (int): id which identifies a product in the database.
    Returns:
        Redirects to home url if not superuser.
        Redirects to products page upon successful delete.
    """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.POST:
        product.delete()
        messages.info(request, 'Product deleted!')
    else:
        messages.error(request, 'That is not allowed!')
    return redirect(reverse('products'))


@login_required
def add_product_review(request, product_id):
    """ A view to add a product review of a particular product.

    Args:
        request (object): HTTP request object.
        product_id (int): id which identifies a product in the database.
    Returns:
        Redirects to product_detail page upon successful review.
    """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        review_form = ProductReviewForm(request.POST)

        if review_form.is_valid():
            already_reviewed = ProductReview.objects.filter(product=product,
                                                            user=request.user)
            if not already_reviewed:
                ProductReview.objects.create(
                    product=product,
                    user=request.user,
                    body=request.POST['body'],
                    review_rating=request.POST['review_rating'],
                )
                messages.info(request, 'Successfully added a review!')
            else:
                messages.error(request, 'Already reviewed!')
            return redirect(reverse('product_detail', args=[product.id]))

        messages.error(request, 'Failed to add product review. Please ensure the \
                       form is valid.')
    return redirect(reverse('product_detail', args=[product.id]))

@login_required
def edit_product_review(request, product_id, review_author):
    """ A view to edit a product review.

    Args:
        request (object): HTTP request object.
        product_id (int): id which identifies a product in the database.
        review_author (str): The request user's username.
    Returns:
        Renders the edit_product_review template.
        Redirects to product_detail page upon successful review.
        Redirects to home url if not superuser or the review author.
    """
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(
        ProductReview, product=product, user__username=review_author)

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

        messages.error(request, 'Failed to edit review. Please ensure the \
                       form is valid.')
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
    """ A view to delete a product review.

    Args:
        request (object): HTTP request object.
        product_id (int): id which identifies a product in the database.
        review_author (str): The request user's username.
    Returns:
        Redirects to product_detail page upon successful or failed delete.
        Redirects to home url if not superuser or the review author.
    """
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(
        ProductReview, product=product, user__username=review_author)

    if request.user != review.user and not request.user.is_superuser:
        messages.error(request, "Sorry, you don't have permission to do that.")
        return redirect(reverse('home'))
    if request.POST:
        review.delete()
        messages.info(request, 'Review deleted!')
    else:
        messages.error(request, 'That is not allowed!')
    return redirect(reverse('product_detail', args=[product.id]))


@require_POST
@login_required
def upvote_product_review(request, product_id, review_author):
    """ A view to upvote a product review.

    Checks if the request user is already in the upvote list and if not
    adds them and increments the review upvote_count.

    Args:
        request (object): HTTP request object.
        product_id (int): id which identifies a product in the database.
        review_author (str): The request user's username.
    Returns:
        A HttpResonse status 200.
    """
    product = get_object_or_404(Product, pk=product_id)
    review = get_object_or_404(
        ProductReview, product=product, user__username=review_author)

    if request.user == review.user:
        messages.error(request, "You can't like your own review!!")
        return HttpResponse(status=200)

    if not review.upvote_list.filter(id=request.user.id):
        review.upvote_list.add(request.user)
        review.upvote_count = review.upvote_list.all().count()
        review.save()
        messages.info(request, 'Liked Review!')
        return HttpResponse(status=200)

    messages.info(request, 'Already Liked!')
    return HttpResponse(status=200)


@login_required
def product_tags_admin(request):
    """ A view to render and edit product genres and promotions fields.

    Checks if the new field already exists and if not, adds it.

    Args:
        request (object): HTTP request object.
    Returns:
        Renders the product_tags_admin page.
        Redirects to product_tags_admin page upon successful add.
        Redirects to home url if not superuser.
    """
    if not request.user.is_superuser:
        messages.error(request, "Sorry, you don't have permission to do that.")
        return redirect(reverse('home'))

    if request.method == 'POST':
        if 'genre' in request.POST:
            new_genre = request.POST['name']
            genres = Genre.objects.filter(name=new_genre)
            genre_form = GenreForm(request.POST)

            if genres:
                messages.error(request, 'Genre already exists!')
            elif genre_form.is_valid():
                genre_form.save()
                messages.info(request, 'Genre Added!')
            else:
                messages.error(request, 'Failed to add genre. Please ensure the \
                            form is valid.')
        if 'promotion' in request.POST:
            new_promotion = request.POST['name']
            promotions = Promotion.objects.filter(name=new_promotion)
            promotion_form = PromotionForm(request.POST)

            if promotions:
                messages.error(request, 'Promotion already exists!')
            elif promotion_form.is_valid():
                promotion_form.save()
                messages.info(request, 'Promotion Added!')
            else:
                messages.error(request, 'Failed to add promotion. Please ensure the \
                            form is valid.')
        return redirect(reverse('product_tags_admin'))

    genre_form = GenreForm()
    promotion_form = PromotionForm()

    template = 'products/product_tags_admin.html'
    context = {
        'genre_form': genre_form,
        'promotion_form': promotion_form,
    }
    return render(request, template, context)
