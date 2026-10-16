from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import PrivateProjectRequest, Project

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

class PrivateProjectRequestForm(forms.ModelForm):
    class Meta:
        model = PrivateProjectRequest
        fields = ("title", "brief", "budget_usd", "desired_delivery_days")
        widgets = {"brief": forms.Textarea(attrs={"rows": 6}), "budget_usd": forms.NumberInput(attrs={"min": "0", "step": "0.01"}), "desired_delivery_days": forms.NumberInput(attrs={"min": "1"})}

class OrderForm(forms.Form):
    project = forms.ModelChoiceField(queryset=Project.objects.none())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["project"].queryset = Project.objects.filter(is_published=True)
