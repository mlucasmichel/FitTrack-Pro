from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import MealLog, Meal
from .forms import MealLogForm, CustomMealForm


@login_required
def nutrition_hub(request):
    today = timezone.now().date()

    # Handle Form Submissions
    if request.method == 'POST':
        if 'log_meal' in request.POST:
            log_form = MealLogForm(request.POST, user=request.user)
            if log_form.is_valid():
                meal_log = log_form.save(commit=False)
                meal_log.user = request.user
                meal_log.save()
                messages.success(request, "Meal logged successfully!")
                return redirect('nutrition_hub')

        elif 'create_meal' in request.POST:
            custom_form = CustomMealForm(request.POST)
            if custom_form.is_valid():
                new_meal = custom_form.save(commit=False)
                new_meal.created_by = request.user
                new_meal.save()

                MealLog.objects.create(
                    user=request.user, meal=new_meal, servings=1)
                messages.success(
                    request, f"{new_meal.name} created and logged!")
                return redirect('nutrition_hub')

    log_form = MealLogForm(user=request.user)
    custom_form = CustomMealForm()

    # Get all logs for today
    todays_logs = MealLog.objects.filter(
        user=request.user, logged_at__date=today).select_related('meal').order_by('-logged_at')

    # Calculate Totals
    total_cals = sum(log.total_calories for log in todays_logs)
    total_protein = sum(log.total_protein for log in todays_logs)
    total_carbs = sum(log.total_carbs for log in todays_logs)
    total_fats = sum(log.total_fat for log in todays_logs)

    goals = {'calories': 2500, 'protein': 150, 'carbs': 300, 'fats': 80}

    nutrition_data = {
        'consumed': {
            'calories': total_cals, 'protein': total_protein,
            'carbs': total_carbs, 'fats': total_fats
        },
        'goals': goals
    }

    context = {
        'todays_logs': todays_logs,
        'nutrition_data': nutrition_data,
        'log_form': log_form,
        'custom_form': custom_form,
    }
    return render(request, 'nutrition/hub.html', context)
