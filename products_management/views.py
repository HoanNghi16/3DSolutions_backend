from rest_framework import request
from rest_framework.generics import RetrieveAPIView, ListAPIView
from .models import Products, Materials, Categories
from .pagination import ProductsPagination
from .serializer import ProductsSerializer, ProductDetailsSerializer, MaterialsSerializer, ProductMaterialSerializer, \
    CategoriesSerializer

def get_all_children(category):
    ids = [category.id]
    for child in category.children.all():
        print(child)
        ids += get_all_children(child)
    return ids
# Create your views here.
class ProductsView(ListAPIView):
    #queryset = Products.objects.all().order_by("-id")
    pagination_class = ProductsPagination
    serializer_class = ProductsSerializer
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')
        sort = self.request.query_params.get('sort')
        cate = self.request.query_params.get('category')
        products = Products.objects.all()


        if cate:
            category = Categories.objects.get(id=cate)
            child_ids = get_all_children(category)
            products = products.filter(category_id__in =child_ids)

        if keyword != "None" and keyword:
            key_list = keyword.strip()
            for key in key_list:
                products = products.filter(name__icontains=key)
        if sort != "None" and sort:
            if sort == "up":
                products = products.order_by('unit_price')
            else:
                products = products.order_by('-unit_price')

        return products

class DetailsView(RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductDetailsSerializer
    lookup_field = 'id'


class MaterialsView(ListAPIView):
    queryset = Materials.objects.all().order_by("-id")
    serializer_class = ProductMaterialSerializer

class CategoriesView(ListAPIView):
    def get_queryset(self):
        query_set = Categories.objects.filter(parent = None)
        return query_set
    serializer_class = CategoriesSerializer