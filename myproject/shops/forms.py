from django import forms
from .models import StoreManagement


class StoreManagementModelForm(forms.ModelForm):
    class Meta:
        model = StoreManagement
        fields = "__all__"
