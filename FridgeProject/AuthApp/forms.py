from AuthApp.models import CustomUser
from FridgeApp.forms import forms

class CustomUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'id_password'}),
        label="Password"
    )
    password_confirmed = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'id_password_confirmed'}),
        label="Confirm Password"
    )
    role = forms.ChoiceField(
        widget=forms.Select(attrs={'id': 'id_role'}),
        initial=CustomUser.Role.USER,
        label="Role",
        choices=CustomUser.Role.choices
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmed = cleaned_data.get('password_confirmed')

        if password != password_confirmed:
            self.add_error('password_confirmed', "Passwords do not match.")

        return cleaned_data

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            self.add_error("username", f"User with {username} exists")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            self.add_error("email", f"User with {email} exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(max_length=256, label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if not CustomUser.objects.filter(username=username).exists():
            self.add_error("username", f"User with {username} does not exist")
        return username


