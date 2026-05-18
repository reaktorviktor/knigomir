from django.contrib import admin
from .models import Category, Author, Book, Review, Cart, CartItem, Order, OrderItem, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name']
    search_fields = ['first_name', 'last_name']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['book', 'quantity', 'price']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'price', 'stock', 'available', 'featured']
    list_filter = ['available', 'featured', 'category']
    list_editable = ['price', 'stock', 'available', 'featured']
    search_fields = ['title', 'author__first_name', 'author__last_name']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created']
    list_filter = ['rating']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'status', 'total_price', 'created']
    list_filter = ['status']
    list_editable = ['status']
    search_fields = ['user__username', 'full_name', 'email']
    inlines = [OrderItemInline]


admin.site.register(Cart)
admin.site.register(Wishlist)
