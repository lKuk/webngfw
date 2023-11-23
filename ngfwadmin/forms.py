from django import forms
from ngfwadmin.models import Device
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.core.validators import validate_ipv46_address
from django.utils.safestring import mark_safe
from django.forms.utils import ErrorList


class DivErrorList(ErrorList):
    def __str__(self):
        return self.as_divs()

    def as_divs(self):
        if not self: return ''
        return mark_safe('<div class="errorlist">%s</div>' % ''.join(['<div class="invalid-feedback d-block">%s</div>' % e for e in self]))


# Устройства NGFW
class ConnectForm(forms.ModelForm):
    ip = forms.CharField(max_length=255,
                         label='IP адрес',
                         initial='192.168.3.35',
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

    class Meta:
        model = Device
        fields = ["ip", "port", "login", "password"]
