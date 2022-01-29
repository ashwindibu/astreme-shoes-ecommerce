from django.db import models
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from django.forms import ModelForm, fields

class CreateUserForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ['firstname','secondname','email','phone','password1','password2']