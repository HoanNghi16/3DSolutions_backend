from time import strptime
from datetime import date, datetime
from .models import Users, UserAccounts
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
        self.valid_data = None
        self._error = None

    def is_valid(self):
        name = self.valid_name()
        email = self.valid_email()
        phone = self.valid_phone()
        date_of_birth = self.valid_date_of_birth()
        if name and email and phone and date_of_birth:
            self.valid_data = {'email': email,
                               'name':name,
                               'date_of_birth': date_of_birth,
                               'password': self.password,
                               'phone': phone}
            return True
        else:
            self._error = 'Invalid data ' + f'name : {name}, email : {email}, phone : {phone}, date_of_birth: {date_of_birth}'
            return False

    def valid_date_of_birth(self):
        format_date = '%d/%m/%Y'
        date_of_birth = datetime.strptime(self.date_of_birth, format_date).date()
        today = date.today()
        if(today.year - date_of_birth.year < 18):
            return False
        else:
            return date_of_birth

    def valid_phone(self):
        pattern = r'^0{1}[3-9]{1}\d{8,9}$'
        phone = str(self.phone)
        if(re.fullmatch(pattern, phone)):
            return phone
        else:
            return False

    def valid_name(self):
        pattern = r'^[A-ZÀ-ỸĐ][a-zà-ỹđ]*\s([A-ZÀ-ỸĐ][a-zà-ỹđ]*)(\s[A-ZÀ-ỸĐ][a-zà-ỹđ]*)*$'
        name = self.name
        if(re.match(pattern, name)):
            return name
        else: return False

    def valid_email(self):
        users = UserAccounts.objects.filter(email=self.email)
        if(users.exists()):
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
        if(self.is_valid()):
            valid_data = self.valid_data
            if (self.check_exist()):
                profile =  Users.objects.get(name= valid_data.get('name'), phone = valid_data.get('phone'), date_of_birth= valid_data.get('date_of_birth'))
            else:
                profile_data = {"name": valid_data.get('name'), "phone": valid_data.get('phone'), "date_of_birth": valid_data.get('date_of_birth')}
                account_data = {"email": valid_data.get('email'), "password": valid_data.get('password')}

                profile = Users.objects.create(**profile_data)
            useraccount = UserAccounts.objects.create_user(profile = profile, **account_data)
            return useraccount
        self._error = 'Invalid data'
        return None
    def __str__(self):
        return str(self.valid_data)

class UserInformationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class UserAccountsSerializer(serializers.ModelSerializer):
    profile = UserInformationsSerializer(read_only=True)
    class Meta:
        model = UserAccounts
        fields = '__all__'