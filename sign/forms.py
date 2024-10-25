from allauth.account.forms import LoginForm, SignupForm
from allauth.utils import get_username_max_length
from django import forms
from django.contrib.auth import get_user_model, login
from django.forms import CharField
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomLoginForm(LoginForm):
    password = CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={
                "placeholder": _("Password"),
                "autocomplete": "current-password",
                "class": "form-control rounded-4"
            }
        )
    )
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        login_widget = forms.TextInput(
            attrs={
                "placeholder": _("Username"),
                "autocomplete": "username",
                "class": "form-control rounded-4"
            },
        )
        login_field = forms.CharField(
            label=_("Username"),
            widget=login_widget,
            max_length=get_username_max_length(),
        )

        self.fields["login"] = login_field

    def clean_login(self):
        login_or_email = self.cleaned_data['login']
        if '@' in login_or_email:
            email = login_or_email
            login = None
        else:
            login = login_or_email
            email = None
        if login:
            if not User.objects.filter(username=login).first():
                raise forms.ValidationError('No such username')
        elif email:
            if not User.objects.filter(email=email).first():
                raise forms.ValidationError('No such email address')
        return login_or_email

    def clean_password(self):
        password = self.cleaned_data['password']
        login_or_email = self.cleaned_data.get('login')

        if login_or_email:
            if '@' in login_or_email:
                if not User.objects.filter(email=login_or_email).first().check_password(password):
                    raise forms.ValidationError('Passwod is incorrect')
            else:
                if not User.objects.filter(username=login_or_email).first().check_password(password):
                    raise forms.ValidationError('Passwod is incorrect')

        return password


class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields["password1"] = CharField(
            label=_("Password"),
            widget=forms.PasswordInput(attrs={
                "placeholder": _("Password"),
                'autocomplete': "new-password",
                'class': 'form-control rounded-4'
            })
        )

        self.fields['password2'] = CharField(
            label=_("Password (again)"),
            widget=forms.PasswordInput(attrs={
                "placeholder": _("Password (again)"),
                'class': 'form-control rounded-4'
            })
        )

        self.fields["username"] = forms.CharField(
            label=_("Username"),
            widget=forms.TextInput(
                attrs={
                    "placeholder": _("Username"),
                    "autocomplete": "username",
                    "class": "form-control rounded-4"
                },
            ),
            max_length=get_username_max_length(),
        )

        self.fields["email"] = forms.CharField(
            label=_("E-mail address"),
            widget=forms.TextInput(
                attrs={
                    "placeholder": _("E-mail address"),
                    "autocomplete": "email",
                    "class": "form-control rounded-4"
                },
            ),
            max_length=get_username_max_length(),
        )

    def clean_email(self):
        email = self.cleaned_data['email']

        if '@' not in email or '.' not in email:
            raise forms.ValidationError('Email address must be a valid email address')
        elif User.objects.filter(email=email):
            raise forms.ValidationError('Email address is already in use')

        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data.get('email')

        if username == email:
            raise forms.ValidationError('User name must differ from user email')
        elif User.objects.filter(username=username):
            raise forms.ValidationError('Username is already in use')

        return username

    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        elif password1.islower():
            raise forms.ValidationError('Password must contain at least one capital letter')
        elif len(password1) < 8:
            raise forms.ValidationError('Password should be at least 8 characters')

        return self.cleaned_data