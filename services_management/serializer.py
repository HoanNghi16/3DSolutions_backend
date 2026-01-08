from rest_framework import serializers

from services_management.models import ServiceOrderDetails, ServiceOrderHeaders


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        queryset = ServiceOrderDetails.objects.all()
        fields = '__all__'

class ServiceOrderHeadersSerializer(serializers.ModelSerializer):
    class Meta:
        queryset = ServiceOrderHeaders.objects.all()
        fields = '__all__'

class ServiceOrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        queryset = ServiceOrderDetails.objects.all()

class ServiceOrdersSerializer(serializers.ModelSerializer):
    details = ServiceOrderDetailsSerializer(many=True)
    class Meta:
        queryset = ServiceOrderHeaders.objects.all()
        fields = ['id', 'total', 'details']