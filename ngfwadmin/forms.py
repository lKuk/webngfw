from django import forms
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.core.validators import validate_ipv46_address


# Устройства NGFW
class ConnectForm(forms.Form):
    ip = forms.CharField(max_length=255,
                         label='IP адрес',
                         initial='192.168.3.250',
                         validators=[validate_ipv46_address],
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    port = forms.IntegerField(label='Порт',
                              initial='18888',
                              validators=[MinValueValidator(1000), MaxValueValidator(65535)],
                              widget=forms.TextInput(attrs={'class': 'form-control'}))
    login = forms.CharField(max_length=255,
                            label='Логин',
                            initial='admin',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=255,
                               label='Пароль',
                               initial='111111',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))
