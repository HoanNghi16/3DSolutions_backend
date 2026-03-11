from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from users_management.authenticate import CookieAuthenticateJWT
from .cloudinary_service import upload_image, delete_image
from .models import CustomerUploaded


class FileUploadView(APIView):
    authentication_classes = [CookieAuthenticateJWT]
    def post(self, request):
        try:
            if not request.user.is_authenticated:
                raise Exception('Vui lòng đăng nhập để sử dụng chức năng này!')
            account = request.user
            file = request.FILES["file"]
            if not file:
                raise Exception('Vui lòng chọn file!')
            type = request.data["type"]
            if type == 'avt':
                result = upload_image(file=file, folder=type)
                if not result:
                    raise Exception('Lỗi!')
                else:
                    term = CustomerUploaded.objects.create(public_file_id=result['public_id'], type=type, path = result['url'])
                    term.save()
                    old_avt = CustomerUploaded.objects.filter(path = account.avt).first()
                    if old_avt:
                        delete = delete_image('avt/'+old_avt.public_file_id)
                        old_avt.delete()
                        print(delete)
                    account.avt = result['url']
                    account.save()
                    return Response({'message': 'Đổi ảnh đại diện thành công!'}, status=status.HTTP_202_ACCEPTED)
            elif type == 'products':

                raise Exception("Chức năng này chưa được hoàn thiện!")
        except Exception as e:
            print(e)
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

