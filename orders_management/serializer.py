from orders_management.models import OrderHeaders, OrderDetails
from rest_framework import serializers
from products_management.serializer import ProductsSerializer
from users_management.models import Users
from products_management.models import Products


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = ProductsSerializer(read_only=True)
    class Meta:
        model = OrderDetails
        fields = ['product', 'quantity']
class OrderList:
    def __init__(self, user):
        if (type(user) == Users):
            self.user = user

    def getHeaders(self):
        return OrderHeaders.objects.filter(user=self.user)

    def result(self):
        heads = self.getHeaders()
        if (len(heads) == 0):
            return None
        re = {}
        query = OrderDetails.objects
        for head in heads:
            detail = query.filter(header = head)
            serializer = OrderDetailsSerializer(detail, many=True)
            re[str(head.id)] = serializer.data
        return re