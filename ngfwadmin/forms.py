from django import forms
from ngfwadmin.models import *
from django.core.validators import *


# Устройства NGFW
class ConnectForm(forms.ModelForm):
    ip = forms.CharField(max_length=255,
                         label='IP адрес',
                         initial='192.168.1.145',
                         widget=forms.TextInput(attrs={'class': 'form-control'}))
    port = forms.CharField(max_length=255,
                           label='Порт',
                           initial='18888',
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    login = forms.CharField(max_length=255,
                            label='Логин',
                            initial='admin',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=255,
                               label='Пароль',
                               initial='111111',
                               widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'password'}))

    class Meta:
        model = Device
        fields = ["ip", "port", "login", "password"]

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        validate_ipv46_address(ip)

    def clean_port(self):
        port = self.cleaned_data['port']
        MaxValueValidator(port, 65535)