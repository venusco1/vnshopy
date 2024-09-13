from django.shortcuts import render, get_object_or_404
from apps.products.models import Category, Product, Subcategory
from . forms import SearchForm , FilterForm



def products(request, category_id=None, subcategory_id=None):
    # Get category and subcategory if IDs are provided
    category = None
    subcategory = None
    search_query = request.GET.get('search', '')

    # Instantiate forms
    search_form = SearchForm(request.GET or None)
    filter_form = FilterForm(request.GET or None)

    products = Product.objects.all()

    # Apply search filtering
    if search_query:
        products = products.filter(product_name__icontains=search_query)

    # Apply category and subcategory filtering
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)
        if subcategory_id:
            subcategory = get_object_or_404(Subcategory, id=subcategory_id)
            products = products.filter(subcategory=subcategory)
    elif subcategory_id:
        subcategory = get_object_or_404(Subcategory, id=subcategory_id)
        products = products.filter(subcategory=subcategory)

    # Handle filter form
    if filter_form.is_valid():
        form_category = filter_form.cleaned_data.get('category')
        form_subcategory = filter_form.cleaned_data.get('subcategory')
        if form_category:
            products = products.filter(category=form_category)
        if form_subcategory:
            products = products.filter(subcategory=form_subcategory)

    # Order categories and subcategories alphabetically
    categories = Category.objects.all().order_by('cat_name')
    subcategories = Subcategory.objects.all().order_by('subcat_name')

    context = {
        'categories': categories,
        'products': products.order_by('product_name'),
        'subcategories': subcategories,
        'category': category,
        'subcategory': subcategory,
        'search_form': search_form,
        'filter_form': filter_form
    }

    return render(request, 'products/home.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    categories = Category.objects.all().order_by('cat_name')
    subcategories = Subcategory.objects.all().order_by('subcat_name')
    search_form = SearchForm(request.GET or None)
    context = {
        'product': product,
        'categories': categories,
        'subcategories': subcategories,
        'search_form': search_form
    }
    return render(request, 'products/product_detail.html', context)