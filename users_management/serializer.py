from time import strptime
from datetime import date, datetime

from carts_management.models import CartHeaders, CartDetails
from .models import Users, UserAccounts, Address
import re
from rest_framework import serializers

class UsersSerializer:
    def __init__(self, data):
        self.data = data
        self.name = data.get("name")
        self.email = data.get("email")
        self.password = data.get("password")
        self.phone = data.get("phone")
        self.date_of_birth = data.get("date_of_birth")
        self.valid_data = {}
        self._error = None


    def is_valid(self, account):
        name = self.valid_name()
        email = self.valid_email() if not account or account.email != self.email else account.email
        phone = self.valid_phone() if not account or account.profile.phone != self.phone else account.profile.phone
        date_of_birth = self.valid_date_of_birth()
        if name and email and phone and date_of_birth:
            self.valid_data = {'email': email,
                               'name': name,
                               'date_of_birth': date_of_birth,
                               'password': self.password,
                               'phone': phone}
            return True
        else:
            return False

    def valid_date_of_birth(self):
        if (self.date_of_birth):
            format_date = '%d/%m/%Y'
            date_of_birth = datetime.strptime(self.date_of_birth, format_date).date()
            today = date.today()
            if(today.year - date_of_birth.year < 12):
                return False
            else:
                self.valid_data['date_of_birth'] = date_of_birth
                return date_of_birth
        return False

    def valid_phone(self):
        pattern = r'^0{1}[3-9]{1}\d{8,9}$'
        phone = str(self.phone)
        if(re.fullmatch(pattern, phone)):
            if (Users.objects.filter(phone=phone).exists()):
                self._error = "Số điện thoại đã được sử dụng."
                return False
            self.valid_data = {'phone': phone}
            return phone
        else:
            self._error = "Số điện thoại không hợp lệ"
            return False

    def valid_name(self):
        pattern = r'^[A-ZÀ-ỸĐ][a-zà-ỹđ]*\s([A-ZÀ-ỸĐ][a-zà-ỹđ]*)(\s[A-ZÀ-ỸĐ][a-zà-ỹđ]*)*$'
        name = self.name
        if(re.match(pattern, name)):
            self.valid_data['name'] = name
            return name
        else: return False

    def valid_email(self):
        users = UserAccounts.objects.filter(email=self.email)
        if(users.exists()):
            self._error  = "Email đã tồn tại"
            return False
        else:
            return self.email


    def check_exist(self):
        valid_data = self.valid_data
        users = Users.objects.filter(name= valid_data.get('name')).filter(date_of_birth= valid_data.get('date_of_birth')).filter(phone= valid_data.get('phone'))
        if(users):
            return True
        else:
            return False

    def create(self):
        if(self.is_valid(account=None)):
            valid_data = self.valid_data
            if (self.check_exist()):
                profile =  Users.objects.get(name= valid_data.get('name'), phone = valid_data.get('phone'), date_of_birth= valid_data.get('date_of_birth'))
            else:
                profile_data = {"name": valid_data.get('name'), "phone": valid_data.get('phone'), "date_of_birth": valid_data.get('date_of_birth')}
                account_data = {"email": valid_data.get('email'), "password": valid_data.get('password')}

                profile = Users.objects.create(**profile_data)
            useraccount = UserAccounts.objects.create_user(profile = profile, **account_data)
            return useraccount
        self._error = 'Dữ liệu không hợp lệ'
        return None
    def __str__(self):
        return str(self.valid_data)

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class UserInformationsSerializer(serializers.ModelSerializer):
    print('serr')
    address = AddressSerializer(many=True)
    date_of_birth = serializers.SerializerMethodField()
    class Meta:
        model = Users
        fields = ['user_id', 'name', 'phone', 'date_of_birth', 'address']
    def get_date_of_birth(self, obj):
        date = obj.date_of_birth
        return date.strftime('%d/%m/%Y')

class UserAccountsSerializer(serializers.ModelSerializer):
    profile = UserInformationsSerializer(read_only=True)
    cart_count = serializers.SerializerMethodField()
    class Meta:
        model = UserAccounts
        fields = ['id', 'avt', 'email', 'profile', 'last_login', 'is_active', 'is_superuser', 'is_staff', 'cart_count']

    def get_cart_count(self,obj):
        header = CartHeaders.objects.get(account = obj)
        count = CartDetails.objects.filter(header = header).count()
        return count if count else 0

class AccountsAdminSerializer(serializers.ModelSerializer):
    profile = UserInformationsSerializer(read_only=True)
    last_login = serializers.SerializerMethodField()
    class Meta:
        model = UserAccounts
        fields = ['id','email', 'avt', 'profile', 'last_login', 'is_active', 'is_superuser', 'is_staff']
    def get_last_login(self, obj):
        ll = obj.last_login
        if ll is None:
            return None
        return ll.strftime('%d/%m/%Y')

