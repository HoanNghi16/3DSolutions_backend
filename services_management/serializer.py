from rest_framework import serializers

from services_management.models import ServiceOrderDetails, ServiceOrderHeaders, Services


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = '__all__'

class ServiceOrderHeadersSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrderHeaders
        fields = '__all__'

class ServiceOrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrderDetails
        fields = '__all__'

class ServiceOrdersSerializer(serializers.ModelSerializer):
    details = ServiceOrderDetailsSerializer(many=True)
    class Meta:
        model = ServiceOrderHeaders
        fields = ['id', 'total', 'details']