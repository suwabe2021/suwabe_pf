#ユーザー登録用フォーム
#今後の機能追加用。現在は使ってないです
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

User = get_user_model()

#新規ユーザー用
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="パスワード", widget=forms.PasswordInput)
    password2 = forms.CharField(label="パスワード(確認用)", widget=forms.PasswordInput)

    class Meta():
        model = User
        fields = ('username', 'email')
        labels = {
            'username': '名前',
            'email': 'メールアドレス',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("パスワードが一致しません")
        return cleaned_data
    
    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserActivateForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput())


class LoginForm(forms.Form):
    email = forms.EmailField(label="メールアドレス")
    password = forms.CharField(label="パスワード", widget=forms.PasswordInput())


#ユーザー編集用
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label="パスワード")

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password', 'is_active', 'is_staff', 'is_superuser'
        )
    
    def clean_password(self):
        return self.instance.password


class PasswordChangeForm(forms.ModelForm):
    
    confirm_password = forms.CharField(
        label='パスワード再設定', widget=forms.PasswordInput()
    )
    
    class Meta:
        model = User
        fields = ('password',)
        labels = {'password': 'パスワード',}
        widgets = {
            'password': forms.PasswordInput()
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValueError("パスワードが一致しません")

    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user