from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserApp as User     

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role']