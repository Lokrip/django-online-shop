"""
All URLs for this application 
are stored here
"""
from rest_framework.routers import DefaultRouter

from django.urls import path, include
from . import views
from . import api


""""
"app_name" is the name that Django needs in 
the URL that will chronize the child 
element"""

app_name = 'product'


routerProduct = DefaultRouter()
routerProduct.register(r'product', api.ProductApiView, basename='product')

routerCategories = DefaultRouter()
routerCategories.register(r'categories', api.CategoryApiView, basename='categories')

urlpatterns = [
    path('', views.HomeView.as_view(), name='product-home'),
    path('store/', views.StoreView.as_view(), name='store'),
    path(
        'store/catalog/<slug:detail_slug>/', 
        views.StoreDetailView.as_view(),
        name='store-detail'
    ),
    path(
        'category/<slug:cat_slug>/', 
        views.StoreCategoryView.as_view(),
        name='store-category'
    ),
    
    path('add/post/', views.StoreCreateProductView.as_view(), name='product-create'),
    path('test/', views.TestTranslation.as_view()),
    
    #api
    
    path('api/v1/', include(routerProduct.urls)),
    path('api/v1/list/', include(routerCategories.urls)),
]

