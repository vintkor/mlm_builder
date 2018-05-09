from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.validators import validate_slug
from phonenumber_field.formfields import PhoneNumberField
from ckeditor.widgets import CKEditorWidget


class AuthForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.PasswordInput()

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileEditForm(forms.Form):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия', required=False)
    email = forms.EmailField(label='Email')
    avatar = forms.ImageField(label='Аватар', required=False)
    website = forms.URLField(label='Сайт', required=False)
    phone = PhoneNumberField(label='Телефон', required=False)
    skype = forms.CharField(label='Skype', required=False, validators=[validate_slug])
    birth_date = forms.DateField(label='День рожденья', required=False)
    link_vkontakte = forms.URLField(label='VK', required=False)
    link_facebook = forms.URLField(label='FACEBOOK', required=False)
    link_twitter = forms.URLField(label='TWITTER', required=False)
    link_instagram = forms.URLField(label='INSTAGRAM', required=False)
    link_odnoklassniki = forms.URLField(label='ODNOKLASNIKI', required=False)
    link_my_world = forms.URLField(label='МОЙ МИР', required=False)
    description = forms.CharField(widget=CKEditorWidget(), label='Обо мне', required=False)

    def __init__(self, *args, **kwargs):
        self.desc_init = kwargs.pop('desc_init', None)
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        self.initial['description'] = self.desc_init
