from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from .models import Book, Category, Author, Cart, CartItem, Order, OrderItem, Review, Wishlist
from .forms import ReviewForm, OrderForm, SearchForm


def index(request):
    featured_books = Book.objects.filter(featured=True, available=True)[:8]
    new_books = Book.objects.filter(available=True).order_by('-created')[:8]
    categories = Category.objects.all()
    popular_books = Book.objects.filter(available=True).annotate(
        avg_rating=Avg('reviews__rating')
    ).order_by('-avg_rating')[:4]

    context = {
        'featured_books': featured_books,
        'new_books': new_books,
        'categories': categories,
        'popular_books': popular_books,
    }
    return render(request, 'store/index.html', context)


def book_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    books = Book.objects.filter(available=True)

    # фильтр по категории
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        books = books.filter(category=category)

    # поиск
    query = request.GET.get('q')
    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query) |
            Q(description__icontains=query)
        )

    # сортировка
    sort = request.GET.get('sort', '-created')
    if sort in ['-created', 'price', '-price', 'title', '-avg_rating']:
        if sort == '-avg_rating':
            books = books.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        else:
            books = books.order_by(sort)

    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
        'books': page_obj,
        'query': query,
        'sort': sort,
    }
    return render(request, 'store/book_list.html', context)


def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, available=True)
    reviews = book.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    related_books = Book.objects.filter(
        category=book.category, available=True
    ).exclude(pk=book.pk)[:4]

    user_review = None
    in_wishlist = False

    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(book=book, user=request.user)
        except Review.DoesNotExist:
            pass
        try:
            wishlist = Wishlist.objects.get(user=request.user)
            in_wishlist = book in wishlist.books.all()
        except Wishlist.DoesNotExist:
            pass

    if request.method == 'POST' and request.user.is_authenticated:
        if user_review:
            messages.warning(request, 'Вы уже оставили отзыв на эту книгу.')
        else:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                messages.success(request, 'Ваш отзыв успешно добавлен!')
                return redirect('store:book_detail', slug=slug)
    else:
        form = ReviewForm()

    context = {
        'book': book,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'related_books': related_books,
        'form': form,
        'user_review': user_review,
        'in_wishlist': in_wishlist,
    }
    return render(request, 'store/book_detail.html', context)


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author=author, available=True)
    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'store/author_detail.html', context)


def author_list(request):
    authors = Author.objects.all()
    context = {'authors': authors}
    return render(request, 'store/author_list.html', context)


def search(request):
    form = SearchForm(request.GET or None)
    books = []
    query = ''
    if form.is_valid():
        query = form.cleaned_data['query']
        books = Book.objects.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query),
            available=True
        )
    return render(request, 'store/search.html', {'form': form, 'books': books, 'query': query})


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    context = {'cart': cart}
    return render(request, 'store/cart.html', context)


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        if item.quantity < book.stock:
            item.quantity += 1
            item.save()
            messages.success(request, f'Количество "{book.title}" обновлено.')
        else:
            messages.warning(request, 'Больше нет в наличии.')
    else:
        messages.success(request, f'"{book.title}" добавлена в корзину!')

    next_url = request.META.get('HTTP_REFERER', '/')
    return redirect(next_url)


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, 'Книга убрана из корзины.')
    return redirect('store:cart_detail')


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0 and qty <= item.book.stock:
        item.quantity = qty
        item.save()
    elif qty <= 0:
        item.delete()
    return redirect('store:cart_detail')


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.warning(request, 'Ваша корзина пуста.')
        return redirect('store:cart_detail')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                comment=form.cleaned_data.get('comment', ''),
                total_price=cart.get_total_price(),
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price,
                )
                # уменьшаем остаток
                item.book.stock -= item.quantity
                item.book.save()

            cart.items.all().delete()
            messages.success(request, f'Заказ #{order.pk} успешно оформлен!')
            return redirect('store:order_detail', pk=order.pk)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['email'] = request.user.email
            initial['full_name'] = request.user.get_full_name()
        form = OrderForm(initial=initial)

    context = {'cart': cart, 'form': form}
    return render(request, 'store/checkout.html', context)


@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_list.html', {'orders': orders})


@login_required
def toggle_wishlist(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if book in wishlist.books.all():
        wishlist.books.remove(book)
        messages.info(request, f'"{book.title}" убрана из избранного.')
    else:
        wishlist.books.add(book)
        messages.success(request, f'"{book.title}" добавлена в избранное!')
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def wishlist(request):
    wish, _ = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist': wish})


def about(request):
    return render(request, 'store/about.html')


def contacts(request):
    return render(request, 'store/contacts.html')
