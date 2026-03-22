from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import MealPlan, Meal, MealLog

User = get_user_model()


class NutritionLogicTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='nutritionist', password='password123')
        self.plan = MealPlan.objects.create(title="High Protein")
        self.meal = Meal.objects.create(
            meal_plan=self.plan, name="Salmon", calories=500, protein_grams=40, carbs_grams=0, fat_grams=35
        )

    def test_meal_log_total_calculation(self):
        """Verify property-based math for servings works correctly"""
        log = MealLog.objects.create(
            user=self.user, meal=self.meal, servings=1.5)
        # 500 * 1.5 = 750
        self.assertEqual(log.total_calories, 750)
        # 40 * 1.5 = 60
        self.assertEqual(log.total_protein, 60)

    def test_custom_meal_ownership(self):
        """Verify created_by field works for user-specific meals"""
        custom = Meal.objects.create(
            name="My Shake", calories=300, created_by=self.user)
        self.assertEqual(custom.created_by, self.user)
        self.assertIsNone(self.meal.created_by)
