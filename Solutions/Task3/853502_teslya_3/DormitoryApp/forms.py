from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.forms import CharField, ModelChoiceField, BooleanField

from .models import User, Room
import logging


def create_groups():
    logger = logging.getLogger('django')
    lodgers, created_lodger = Group.objects.get_or_create(name="Lodger")
    staff, created_staff = Group.objects.get_or_create(name='Personnel')
    if not created_lodger:
        logger.info('Group Lodgers was created early')
    if not created_staff:
        logger.info('Group Personal was created early')


class MyUserCreationFormAdmin(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'telephone', 'faculty', 'room', 'position', 'email')

    def __init__(self, *args, **kwargs):
        super(MyUserCreationFormAdmin, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False


class UserCreationLodgerForm(UserCreationForm):
    middle_name = CharField(required=False, label='Отчество')
    telephone = CharField(required=True, label='Телефон')
    room = ModelChoiceField(queryset=Room.objects.all(), required=False, label='Кабинет/комната')
    faculty = CharField(required=False, label='Факультет')

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name',  'middle_name', 'last_name', 'telephone', 'faculty', 'room', 'email')


class UserCreationPersonnelForm(UserCreationForm):
    middle_name = CharField(required=False, label='Отчество')
    telephone = CharField(required=True, label='Телефон')
    room = ModelChoiceField(queryset=Room.objects.all(), required=False, label='Кабинет/комната')
    position = CharField(required=False, label='Должность')

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name',  'middle_name', 'last_name', 'telephone', 'position', 'room', 'email')


class MyUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = User
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'telephone', 'faculty', 'room', 'position', 'email')

    def __init__(self, *args, **kwargs):
        super(MyUserChangeForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False


class UserLodgerOrPersonnelChangeForm(UserChangeForm):
    middle_name = CharField(required=False, label='Отчество')
    telephone = CharField(required=True, label='Телефон')
    faculty = CharField(required=False, label='Факультет')
    room = ModelChoiceField(queryset=Room.objects.all(), required=False, label='Кабинет/комната')
    position = CharField(required=False, label='Должность')

    class Meta(UserChangeForm):
        model = User
        fields = ('username', 'first_name', 'middle_name', 'last_name', 'telephone', 'faculty', 'room', 'position', 'email')

    def __init__(self, *args, **kwargs):
        super(UserLodgerOrPersonnelChangeForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = False
            self.fields[key].widget.attrs['class'] = 'form_control'


