from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from users_management.authenticate import CookieAuthenticateJWT
from services_management.cloudinary_service import upload_image
from .models import Products, Materials, Categories, ProductImages
from .pagination import ProductsPagination
from .serializer import ProductsSerializer, ProductDetailsSerializer, MaterialsSerializer, ProductMaterialSerializer, \
    CategoriesSerializer
from rest_framework.views import APIView
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


class AdminProduct(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    permission_classes = [IsAdminUser]
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                raise Exception('Vui lòng đăng nhập')
            else:
                name = request.data.get('name', None)
                price = request.data.get('price', None)
                quantity = request.data.get('quantity', None)
                description = request.data.get('description', None)
                if Products.objects.filter(name=name).exists():
                    raise Exception("Sản phẩm đã tồn tại!")
                product = Products.objects.create(name=name, unit_price=price, quantity=quantity, description=description, rate= 0)
                images = request.FILES.getlist('images[]')
                if images:
                    for count, image in enumerate( images):
                        result = upload_image(image, 'products')
                        is_thumbnail = True if count == 0 else False
                        ProductImages.objects.create(product= product, fileID = result['public_id'], path = result['url'], type="img", is_thumbnail=is_thumbnail)
                return Response({'message': 'đã đăng nhập'}, status = status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)