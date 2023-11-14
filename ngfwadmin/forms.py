from django import forms


# Устройства NGFW
class DeviceForm(forms.Form):
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

