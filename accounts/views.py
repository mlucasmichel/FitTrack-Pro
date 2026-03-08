from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    """
    The main internal hub for logged-in users.
    displays quick stats and navigation to workouts/nutrition/subscriptions.
    """
    return render(request, 'dashboard.html')
