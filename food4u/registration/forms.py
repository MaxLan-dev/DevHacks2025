# from django import forms
# from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
# from django.contrib.auth import get_user_model
# from django.core.exceptions import ValidationError

# User = get_user_model()

# class UserRegistrationForm(forms.ModelForm):
#     password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ('email', 'name')  # Only actual model fields
#         # exclude = ('password',) # alternative

#     def __init__(self, *args, **kwargs):
#         self.is_retailer = kwargs.pop('is_retailer', False)
#         super().__init__(*args, **kwargs)

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1")
#         password2 = self.cleaned_data.get("password2")
#         if password1 and password2 and password1 != password2:
#             raise ValidationError("Passwords don't match")
#         return password2

#     # def save(self, commit=True):    # Remove this because ModelForm does this for us.
#     #     user = super().save(commit=False)
#     #     user.set_password(self.cleaned_data["password1"])
#     #     if commit:
#     #         user.save()
#     #     return user

from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('email', 'name')  # Only include fields that exist in your CustomUser model

    def __init__(self, *args, **kwargs):
        self.is_retailer = kwargs.pop('is_retailer', False)
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()


class SetPasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirm new password",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('new_password1')
        password2 = cleaned_data.get('new_password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return cleaned_data


class ChangePasswordForm(PasswordChangeForm):
    pass


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)