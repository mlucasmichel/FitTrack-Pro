from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from workouts.models import WorkoutLog, SetLog
from nutrition.models import MealLog


@login_required
def profile(request):
    """
    Displays the user's profile details and their custom data.
    """
    custom_meals = Meal.objects.filter(created_by=request.user).order_by('-id')

    context = {
        'custom_meals': custom_meals,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def dashboard(request):
    """
    The main internal hub for logged-in users.
    Displays real-time stats from workouts and nutrition.
    """
    today = timezone.now().date()
    one_week_ago = today - timedelta(days=6)

    # --- 1. Nutrition Stats (Today) ---
    todays_meals = MealLog.objects.filter(
        user=request.user, logged_at__date=today)
    daily_calories = sum(log.total_calories for log in todays_meals)

    # --- 2. Workout Stats (Lifetime) ---
    total_workouts = WorkoutLog.objects.filter(user=request.user).count()

    # --- 3. Weekly Activity Chart Data ---
    dates_list = [(one_week_ago + timedelta(days=i)) for i in range(7)]
    chart_labels = [d.strftime('%a') for d in dates_list]
    chart_data = [0] * 7

    # Fetch sets from the last 7 days
    recent_sets = SetLog.objects.filter(
        workout_log__user=request.user,
        workout_log__logged_at__date__gte=one_week_ago
    )

    for s in recent_sets:
        log_date = s.workout_log.logged_at.date()
        if log_date in dates_list:
            index = dates_list.index(log_date)
            chart_data[index] += 1

    context = {
        'daily_calories': daily_calories,
        'total_workouts': total_workouts,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
    }
    return render(request, 'accounts/dashboard.html', context)
