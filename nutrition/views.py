from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import MealLog, Meal
import json


@login_required
def nutrition_hub(request):
    """
    Displays the user's daily calorie calculator and logged meals.
    """
    today = timezone.now().date()

    # Get all logs for today
    todays_logs = MealLog.objects.filter(
        user=request.user,
        logged_at__date=today
    ).select_related('meal')

    # Calculate Totals
    total_cals = sum(log.total_calories for log in todays_logs)
    total_protein = sum(log.total_protein for log in todays_logs)
    total_carbs = sum(log.total_carbs for log in todays_logs)
    total_fats = sum(log.total_fat for log in todays_logs)

    # Hardcoded goals for demonstration (could be user-specific in the future)
    goals = {
        'calories': 2500,
        'protein': 150,
        'carbs': 300,
        'fats': 80
    }

    # data for JS
    nutrition_data = {
        'consumed': {
            'calories': total_cals,
            'protein': total_protein,
            'carbs': total_carbs,
            'fats': total_fats
        },
        'goals': goals
    }

    context = {
        'todays_logs': todays_logs,
        'nutrition_data': nutrition_data, 
    }
    return render(request, 'nutrition/hub.html', context)
