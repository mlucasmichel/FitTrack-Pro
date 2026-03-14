from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class MealPlan(models.Model):
    """
    A curated collection of meals (e.g., '30-Day Keto').
    Premium plans will be restricted via views later.
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_premium = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Meal(models.Model):
    """
    Individual food items or recipes.
    Strict validation prevents negative nutritional values.
    """
    meal_plan = models.ForeignKey(
        MealPlan, on_delete=models.CASCADE, related_name='meals')
    name = models.CharField(max_length=200)

    # Validation
    calories = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    protein_grams = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], default=0)
    carbs_grams = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], default=0)
    fat_grams = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], default=0)

    def __str__(self):
        return f"{self.name} ({self.calories} kcal)"


class MealLog(models.Model):
    """
    Records when a user eats a specific meal.
    Servings multiplier allows for partial or multiple portions.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name='meal_logs')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)

    servings = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=1.0,
        validators=[MinValueValidator(0.1)]  # Can't log 0 or negative servings
    )
    logged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.meal.name} x{self.servings}"

    @property
    def total_calories(self):
        return int(self.meal.calories * self.servings)

    @property
    def total_protein(self):
        return int(self.meal.protein_grams * self.servings)

    @property
    def total_carbs(self):
        return int(self.meal.carbs_grams * self.servings)

    @property
    def total_fat(self):
        return int(self.meal.fat_grams * self.servings)
