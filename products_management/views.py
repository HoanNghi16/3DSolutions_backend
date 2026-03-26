from logging import disable

from django.db import transaction
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from users_management.authenticate import CookieAuthenticateJWT
from services_management.cloudinary_service import upload_image
from .models import Products, Materials, Categories, ProductImages
from .pagination import ProductsPagination
from .serializer import ProductsSerializer, ProductDetailsSerializer, MaterialsSerializer, AdminCateSerializer,CategoriesSerializer
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
        products = Products.objects.filter(disable= False)
        if cate:
            category = Categories.objects.get(id=cate)
            child_ids = get_all_children(category)
            products = products.filter(category_id__in =child_ids)
        if keyword != "None" and keyword:
            key_list = keyword.strip().split(' ')
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
    serializer_class = MaterialsSerializer

class AdminCateView(ListAPIView):
    permission_classes = (IsAdminUser,)
    queryset = Categories.objects.all()
    serializer_class = AdminCateSerializer

class CategoriesView(ListAPIView):
    def get_queryset(self):
        query_set = Categories.objects.filter(parent = None)
        return query_set
    serializer_class = CategoriesSerializer


class AdminProduct(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    permission_classes = [IsAdminUser]

    def put(self, request):
        try:
            with transaction.atomic():
                product = Products.objects.select_for_update().get(id=request.data['id'])
                name = request.data.get('name', product.name)
                description = request.data.get('description', product.description)
                unit_price = request.data.get('unit_price', product.unit_price)
                material = request.data.get('material', product.material)
                category = request.data.get('category', product.category)
                disable = request.data.get('disable', product.disable)
                if product:
                    product.name = name
                    product.description = description
                    product.unit_price = unit_price
                    product.material = material
                    product.category = category
                    product.disable = disable
                    product.save()
                    return Response({'message': 'Cập nhật thành công'},status=status.HTTP_200_OK)
                else:
                    raise Exception("Không tìm thấy sản phẩm!")
        except Exception as e:
            return Response({'message': str(e)},status=status.HTTP_400_BAD_REQUEST)



    def post(self, request):
        try:
            if not request.user.is_authenticated:
                raise Exception('Vui lòng đăng nhập')
            else:
                with transaction.atomic():
                    name = request.data.get('name', None)
                    price = float(request.data.get('price', None))
                    quantity = request.data.get('quantity', None)
                    description = request.data.get('description', None)
                    cate = Categories.objects.get(id = request.data.get('cate', None))
                    mate = Materials.objects.get(id=request.data.get('mate', None))
                    if Products.objects.filter(name=name).exists():
                        raise Exception("Sản phẩm đã tồn tại!")
                    product = Products.objects.create(name=name, unit_price=price, quantity=quantity, description=description, rate= 0, category = cate, material = mate)
                    images = request.FILES.getlist('images[]')
                    if images:
                        for count, image in enumerate( images):
                            result = upload_image(image, 'products')
                            is_thumbnail = True if count == 0 else False
                            ProductImages.objects.create(product= product, fileID = result['public_id'], path = result['url'], type="img", is_thumbnail=is_thumbnail)
                    return Response({'message': 'Thêm sản phẩm thành công!'}, status = status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': str(e)}, status=status.HTTP_403_FORBIDDEN)