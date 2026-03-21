from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import MealLog, Meal, MealPlan
from .forms import MealLogForm, CustomMealForm


@login_required
def nutrition_hub(request):
    today = timezone.now().date()

    is_premium = False
    if hasattr(request.user, 'subscription'):
        is_premium = request.user.subscription.status == 'active'

    meal_plans = MealPlan.objects.all().order_by('title')

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
        'meal_plans': meal_plans,
        'is_premium': is_premium
    }
    return render(request, 'nutrition/hub.html', context)


@login_required
def edit_custom_meal(request, meal_id):
    """
    Allows a user to edit a meal they created.
    """
    meal = get_object_or_404(Meal, id=meal_id, created_by=request.user)

    if request.method == 'POST':
        form = CustomMealForm(request.POST, instance=meal)
        if form.is_valid():
            form.save()
            messages.success(request, f"'{meal.name}' updated successfully.")
            return redirect('profile')
    else:
        form = CustomMealForm(instance=meal)

    context = {
        'form': form,
        'meal': meal
    }
    return render(request, 'nutrition/edit_meal.html', context)


@login_required
def delete_custom_meal(request, meal_id):
    """
    Allows a user to safely delete a custom meal they created.
    Must be a POST request for security.
    """
    meal = get_object_or_404(Meal, id=meal_id, created_by=request.user)

    if request.method == 'POST':
        meal_name = meal.name
        meal.delete()
        messages.success(request, f"'{meal_name}' has been deleted.")
        return redirect('profile')

    return redirect('profile')
