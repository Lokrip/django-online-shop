import uuid

from typing import Any

from django.db.models.query import QuerySet
from django.shortcuts import (
    render, 
    get_object_or_404, 
    redirect
)
from django.views.generic import (
    View
)
from django.db.models import Count
from django.contrib import messages
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.http import (
    HttpRequest,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from settings.context.context_processors import get_header_settings

from utils.mixins import MixinsStore, form_valid
from models.models import (
    Product, 
    ProductImageModel,
    User
)
from .forms import (
    CreatePoroductForm,
    ReviewForm,
)


def get_menu_primary(request: HttpRequest, title: str):
    """
    Retrieves the primary menu based on the request and title.

    Args:
        request (HttpRequest): The HTTP request object.
        title (str): The title used to filter or modify the menu.

    Returns:
        Optional[str]: The active menu header, or a placeholder if not found.

    Raises:
        ValueError: If the menu is not found or title is invalid.
    """
    

    menu = get_header_settings(request)['navbarHeader']
    
    if not menu:
        raise ValueError("Menu not found in request context")
    
    if not isinstance(title, str) or not title:
        raise ValueError("Invalid title provided")
    
    mixins = MixinsStore(title, menu)
    mixins.set_active_menu()
    menu_header = mixins.get_menu()
    
    return menu_header or '<None-menu>'


def create_data_model(form, model_name: str, is_user: bool = False):
    """
    Create a data model based on the given `model_name`. Optionally,
    specify if the model is a user-related model by setting `is_user` to True.

    :param model_name: The name of the model to create.
    :param is_user: Boolean indicating if the model is user-related. Defaults to False.
    :return: The created data model or None if model_name is invalid.
    """
    

class HomeView(ListView, MixinsStore):
    """_summary_

    Args:
        TemplateView (View): View template only

    Returns:
        _type_: _description_
    """
    model = Product
    context_object_name = 'products'
    template_name = 'product/product-home.html'
    
    def get_queryset(self):
        return (Product.objects
        .select_related('category')
        .prefetch_related('color')
        .order_by('-pk')
        )
    
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['popular_products'] = Product.objects.annotate(
            review_count=Count('product_review')
        ).filter(review_count__gt=2)
        return context
    
    def post(self, request):
        self.object_list = self.get_queryset()
        query = request.POST.get('searchPp')
        
        redirect = self._search_page(request, query=query)
        if redirect is not None:
            return redirect
        
        context = self.get_context_data()
        return render(request, self.template_name, context)
        

class StoreView(ListView, MixinsStore):
    """_summary_

    Args:
        View (View All Request): [
            GET,
            POST,
            PUT, 
            PATCH,
            DELETE
        ]
    """
    model = Product
    template_name = 'product/product.html'
    context_object_name = 'products'
    
    def searchStore(self, query) -> QuerySet[Product]:
        """Search for products by name or description."""
        queryset = self.search(Product, query)
        if isinstance(queryset, str) and queryset in ('Product None'):
            return []
        return queryset
    
    def get_queryset(self) -> QuerySet[Any]:
        """
        Retrieve the list 
        of products, optionally filtered by 
        a search query.
        """
        
        query = self.request.GET.get('search-product', '').strip()
        queryset = self.get_queryset_mixins(self.request)
        if query: queryset = self.searchStore(query)

        return queryset
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['navbarHeader'] = get_menu_primary(self.request, 'Store')
        context['title'] = 'Список продуктов'
        return context
    
class StoreCategoryView(ListView, MixinsStore):
    model = Product
    template_name = 'product/product.html'
    context_object_name = 'products'
    
    def get_queryset(self) -> QuerySet[Any]:
        query = self.request.GET.get('search-product', '').strip()
        products = None
        
        if self.kwargs['cat_slug'] != 'all-product':
            products = self.get_queryset_mixins(
                self.request, 
                slug_category=self.kwargs['cat_slug']
            )
        else:
            products = self.get_queryset_mixins(self.request)
        
        if query: 
            products = self.search(Product, query)
            
            if isinstance(products, str) and products in ('Product None'):
                return []
            
        return (products 
                if products.exists or products is not None 
                else []
                )
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['menu_header'] = get_menu_primary(self.request, 'Store')
        context['title'] = 'Список продуктов'
        return context
    
    
class StoreDetailView(View):
    """_summary_
    Args:
        View (View All Request): [
            GET,
            POST,
            PUT, 
            PATCH,
            DELETE
        ]
    """
    def get(self, request: HttpRequest, detail_slug: str):
        product = get_object_or_404(
            Product.objects.select_related('category'),
            slug=detail_slug,
        )
        
        context = {
            'title': product.title,
            'product': product,
            'form': ReviewForm()
        }
        return render(request, 'product/product-detail.html', context)

    def post(self, request: HttpRequest, detail_slug: str):
        if not request.user.is_authenticated:
            messages.error(request, 'вы не авторизованные')
            return redirect("product:store-detail", detail_slug=detail_slug)
        
        form = ReviewForm(request.POST)
        product = get_object_or_404(Product, slug=detail_slug)
        preliminary_stop = form_valid(form, True)
        
        if preliminary_stop is not None:
            preliminary_stop.user = request.user
            preliminary_stop.product = product
            preliminary_stop.save()
            return redirect("product:store-detail", detail_slug=detail_slug)
        else:
            messages.error(request, 'The form is invalid, fill out the form correctly')
        
        context = {
            'title': product.title,
            'product': product,
            'form': ReviewForm()
        }
        return render(request, 'product/product-detail.html', context)


class StoreCreateProductView(LoginRequiredMixin, View):
    """_summary_
    Args:
        View (View All Request): [
            GET,
            POST,
            PUT, 
            PATCH,
            DELETE
        ]
    """
    def get(self, request: HttpRequest):
        form = CreatePoroductForm()
        navbarHeader = get_menu_primary(self.request, 'Create')
        context = {
            "title": "Создание продуктов",
            'navbarHeader': navbarHeader,
            'form': form
        }
        return render(request, 'product/product-create.html', context)
    
    def post(self, request: HttpRequest):
        
        form = CreatePoroductForm(request.POST, request.FILES)
        
        if form.is_valid():
            title = form.cleaned_data.get('title')
            
            temporary_storage = form.save(commit=False)
            temporary_storage.user = request.user
            
            # Добавляем ID пользователя для уникальности
            user_id = request.user.id
            temporary_storage.slug = slugify(f"{title}-{user_id}-{uuid.uuid4().hex[:10]}")
            
            # Сохраняем продукт
            temporary_storage.save()
            
            # Получаем список изоброжений
            images = request.FILES.getlist('image-list')
            
            for image in images:
                ProductImageModel.objects.create(
                    product=temporary_storage,
                    image=image
                )
            
            return redirect('product:store-detail', detail_slug=temporary_storage.slug)
            
        context = {
            "title": "Создание продуктов",
            'form': form
        }
        
        return render(request, 'product/product-create.html', context)


class TestTranslation(View):
    def get(self, request):
        return render(request, 'product/test.html')