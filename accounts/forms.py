from django import forms
from .models import CustomUser


class UserGoalsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['calorie_goal', 'protein_goal', 'carbs_goal', 'fat_goal']
        widgets = {
            'calorie_goal': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'min': '500'}),
            'protein_goal': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'min': '0'}),
            'carbs_goal': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'min': '0'}),
            'fat_goal': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'min': '0'}),
        }
