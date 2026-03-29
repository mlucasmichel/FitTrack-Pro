from django import forms
from .models import CustomUser


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'calorie_goal',
                  'protein_goal', 'carbs_goal', 'fat_goal']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'placeholder': 'Enter last name'}),
            'calorie_goal': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'min': '500'}),
            'protein_goal': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'min': '0'}),
            'carbs_goal': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'min': '0'}),
            'fat_goal': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'min': '0'}),
        }
