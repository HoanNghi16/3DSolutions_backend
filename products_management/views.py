from rest_framework.generics import RetrieveAPIView, ListAPIView
from .models import Products, Materials
from .pagination import ProductsPagination
from .serializer import ProductsSerializer, ProductDetailsSerializer, MaterialsSerializer


# Create your views here.
class ProductsView(ListAPIView):
    queryset = Products.objects.all().order_by("-id")
    pagination_class = ProductsPagination
    serializer_class = ProductsSerializer

class DetailsView(RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductDetailsSerializer
    lookup_field = 'id'

class MaterialsView(ListAPIView):
    queryset = Materials.objects.all().order_by("-id")
    serializer_class = MaterialsSerializer