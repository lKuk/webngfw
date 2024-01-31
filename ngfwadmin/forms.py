from django import forms
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.core.validators import validate_ipv46_address

from ngfwadmin.models import Device


# Устройства NGFW
class ConnectForm(forms.Form):
    login = forms.CharField(max_length=255,
                            label='Логин',
                            initial='',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=255,
                               label='Пароль',
                               initial='',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
    ip = forms.CharField(max_length=255,
                         label='IP адрес',
                         initial='192.168.',
                         validators=[validate_ipv46_address],
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    port = forms.IntegerField(label='Порт',
                              initial='18888',
                              validators=[MinValueValidator(1000), MaxValueValidator(65535)],
                              widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Device
        fields = ["ip", "port", "login", "password"]
