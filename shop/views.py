from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.views.generic import ListView, DetailView
from cart.forms import CartAddProductForm
# from .recommender import Recommender


# Create your views here.
class ProductListView(ListView):
    template_name = 'shop/product/list.html'
    queryset = Product.objects.filter(available=True)
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        category = None
        categories = Category.objects.all()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            self.queryset = self.queryset.filter(category=category)

        # Add in a QuerySet of all the books
        context['category'] = category
        context['categories'] = categories

        return context


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)

    cart_product_form = CartAddProductForm()

    # r = Recommender()
    # recommended_products = r.suggest_products_for([product], 4)

    return render(request,
                  'shop/product/detail.html',
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   # 'recommended_products': recommended_products,
                   })
