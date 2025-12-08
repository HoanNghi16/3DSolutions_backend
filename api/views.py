from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
# Create your views here.

@require_http_methods(['GET'])
def hello_world(request):
    """
    Endpoint thử nghiệm đơn giản: GET /api/hello/
    """
    data= {
        "message":"Hello from django backend",
        "status":"success",
        "version": "1.0"
    }
    return JsonResponse(data, status=200)