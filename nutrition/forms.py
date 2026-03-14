from django import forms
from .models import MealLog, Meal


class MealLogForm(forms.ModelForm):
    class Meta:
        model = MealLog
        fields = ['meal', 'servings']
        widgets = {
            'meal': forms.Select(attrs={'class': 'form-select border-0 bg-light rounded-pill px-4 mb-3'}),
            'servings': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4', 'step': '0.1', 'min': '0.1'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['meal'].queryset = Meal.objects.filter(
                created_by__isnull=True) | Meal.objects.filter(created_by=user)


class CustomMealForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['name', 'calories', 'protein_grams',
                  'carbs_grams', 'fat_grams']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4 mb-3', 'placeholder': 'e.g., Avocado Toast'}),
            'calories': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4 mb-3', 'placeholder': 'Calories'}),
            'protein_grams': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4 mb-3', 'placeholder': 'Protein(g)'}),
            'carbs_grams': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4 mb-3', 'placeholder': 'Carbs (g)'}),
            'fat_grams': forms.NumberInput(attrs={'class': 'form-control border-0 bg-light rounded-pill px-4 mb-3', 'placeholder': 'Fats (g)'}),
        }
