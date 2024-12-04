from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from models.models import (
    Product,
    Categories
)
from models.serializers import (
    CategorySerializers,
    ProductSerializers,
)

class ProductPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 100

class ProductApiView(ViewSet):
    pagination_class = ProductPagination
    
    def list(self, request):
        onSale = request.GET.get('onSale') == 'true'
        queryset = Product.objects.order_by('-pk')
        if onSale:
            queryset = queryset.filter(status='on_sale')
        
        page = self.pagination_class().paginate_queryset(queryset, request)
        if page is not None:
            # If pagination applies, use the paginated data
            serializer = ProductSerializers(page, many=True)
            print(page.paginator)
            return Response({
                "data_set": serializer.data,
                "range_page": page.paginator.num_pages
            }, status=status.HTTP_200_OK)
        
        
        serializer = ProductSerializers(queryset, many=True)
        return Response({
            "data_set": serializer.data,
            "range_page": 1 
        }, status=status.HTTP_200_OK)
        
    def retrieve(self, request, pk=None):
        if pk is None:
            raise ValueError('Not Found PK')
        
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'error': 'Not found Product'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializers(product)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    #+ указывает, что предыдущая часть должна встречаться один или более раз. Таким образом, [^/.]+ будет соответствовать сегменту URL, содержащему один или более символов, но без / и .
    #[^...] задаёт набор символов, которые не должны встречаться в этой части URL.
    @action(methods=['get'], detail=False, url_path='categories/(?P<category_slug>[^/.]+)')
    def product_by_category(self, request, category_slug=None):
        if category_slug is None:
            raise ValueError('Not Found category_slug')
        if category_slug.lower() == 'all-product':
            queryset = Product.objects.order_by('-pk')
        else:
            queryset = Product.objects.filter(category__slug=category_slug)
        serializer = ProductSerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class CategoryApiView(ViewSet):
    def list(self, request):
        try:
            queryset = Categories.objects.order_by('-pk')
        except Categories.DoesNotExist:
            return Response({'error': "Serializer not found!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializers(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        