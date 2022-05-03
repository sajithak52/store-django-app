from django import forms
import requests
from django.contrib.auth import authenticate, login


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

    def clean(self):
        op = forms.Form.clean(self)
        gt = op.get
        username = gt('username')
        password = gt('password')

        print(username, password, 'hhhh')
        if not username or not password:
            return op

        user = authenticate(requests, username=username, password=password)

        if user is None:
            raise forms.ValidationError('Invalid credentials... Please re enter your Username and Password.')

        # noinspection PyAttributeOutsideInit
        self.user = user
        return op

    def login(self, request):
        if hasattr(self, 'user') is False:
            raise Exception('The user is not authenticated.')
        login(request, self.user)
        return self.user


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='Old Password')
    new_password = forms.CharField(label='New Password')
    new_password_retype = forms.CharField(label='Retype Password')

    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        username = kwargs.pop('user', None)
        forms.Form.__init__(self, data, files, *args, **kwargs)
        # self.request = request
        self.username = username

    def clean_old_password(self):
        cleaned_data = self.cleaned_data
        username = self.username.username
        old_password = cleaned_data.get('old_password')

        if authenticate(username=username, password=old_password) is None:
            raise forms.ValidationError('The old password is not valid.')

        return old_password

    def clean_new_password_retype(self):
        cleaned_data = self.cleaned_data
        new_password = cleaned_data.get('new_password')
        new_password_retype = cleaned_data.get('new_password_retype')

        if new_password != new_password_retype:
            raise forms.ValidationError('New Password and Retype Password must be same. ')

        return new_password_retype

    def save(self, request):
        user = self.username
        cleaned_data = self.cleaned_data
        new_password = cleaned_data.get('new_password')
        user.set_password(new_password)
        user.save()


class ContactUSForm(forms.Form):
    name = forms.CharField(required=True)
    mobile = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

