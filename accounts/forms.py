from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm as AuthPasswordChangeForm
from .models import User

# 인스타그램 프로필 수정
# 프로필 사진, 이름, id, 웹사이트, 소개, 이메일, 전화번호, 성별

# 유저 모델에 대한 폼을 사용하려면 
# django.contrib.auth.forms에 정의된 UserCreationForm을 활용하면 된다.
class SignupForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2', 'nickname', 'name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError("이미 등록된 이메일입니다.")
        return email

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("avatar", "name", "nickname", "website_url", "bio", "email", "phone_number", "gender")


class PasswordChangeForm(AuthPasswordChangeForm):
    def clean_new_password1(self):
        old_password = self.cleaned_data.get('old_password')
        new_password1 = self.cleaned_data.get('new_password1')
        if old_password and new_password1:
            if old_password == new_password1:
                raise forms.ValidationError("새로운 암호는 기존 암호와 다르게 입력해주세요.")
        return new_password1