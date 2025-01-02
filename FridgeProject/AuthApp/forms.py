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