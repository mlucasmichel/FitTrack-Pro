from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from nutrition.models import Meal


@login_required
def dashboard(request):
    """
    The main internal hub for logged-in users.
    displays quick stats and navigation to workouts/nutrition/subscriptions.
    """
    return render(request, 'accounts/dashboard.html')


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
