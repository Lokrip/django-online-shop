from django import template
from models.models import (
    Categories,
    TagModel,
    Brand,
    Supplier,
    ColorModel
)
from django.db.models import Count, Q
from settings.context.context_processors import get_filter_price_ranges

register = template.Library()



@register.simple_tag(name='get_cat')
def get_cat(is_with_posts=False):
    if is_with_posts:
        ...
    else:
        categories = (
            Categories.objects
            .annotate(Count('product'))
            .filter(Q(product__count__gt=0) | Q(slug='all-product'))
        )
    return categories if categories.exists() else []



@register.filter
def truncate_chars(value, num_chars):
    """
    Shortens a character to the specified number of characters.
    If the line is longer, add "..." at the end.
    """
    
    if len(value) > num_chars:
        return value[:num_chars] + '...'
    return value

@register.filter
def slice_chars(value: str, slice_char: str):
    """
    Trimming a string for a specific length 
    in Django there is a built-in filter 
    of my type, but I repeated it for practice
    """
    
    if not value:
        return ""
    
    split_slise = slice_char.split(':')
    
    
    try:
        number_one = int(split_slise[0]) if split_slise[0] else 0
        number_two = int(split_slise[1]) if len(split_slise) > 1 and split_slise[1] else None
    except ValueError:
        return value
    
    if number_two is not None:
        return value[number_one:number_two]
    else:
        return value[number_one:]

@register.filter
def correct_prices(value):
    """
    Removes '$' and '+' symbols from the 
    string and joins the parts with '-'.
    """
    
    split_value = value.split(' ')
    result = []
    
    for char in split_value:
        if char != '-':
            char = char.replace('$', '').replace('+', '')
            result.append(char)
    
    return '-'.join(result)
    
    
def get_sort_options(request):
    options = [
        {'label': 'Default', 'value': 'default', 'active': False},
        {'label': 'Popularity', 'value': 'popularity', 'active': False},
        {'label': 'Average rating', 'value': 'rating', 'active': False},
        {'label': 'Newness', 'value': 'newness', 'active': False},
        {'label': 'Price: Low to High', 'value': 'price', 'active': False},
        {'label': 'Price: High to Low', 'value': '-price', 'active': False},
    ]
    current_sort = request.GET.get('sort', 'default')
    for option in options:
        if option['value'] == current_sort:
            option['active'] = True
            
    return options
    
@register.inclusion_tag('product/includes/filter.html')
def get_filter_html(request):
    filterPriceRanges = get_filter_price_ranges()
    tags = TagModel.objects.order_by('-pk')
    brands = Brand.objects.order_by('-pk')
    colors = ColorModel.objects.order_by('-pk')
    suppliers = Supplier.objects.order_by('-pk')
    sort_options = get_sort_options(request)
    
    colorGet = request.GET.get('color', None)
    tagGet = request.GET.get('product-tags', None)
    pricesGet = request.GET.get('prices', None)
    
    
    context = {
        'tags': tags,
        'brands': brands,
        'colors': colors,
        'suppliers': suppliers,
        'sort_options': sort_options,
        'colorGet': colorGet,
        'tagGet': tagGet,
        'filterPriceRanges': filterPriceRanges,
        'pricesGet': pricesGet
    }
    
    return context