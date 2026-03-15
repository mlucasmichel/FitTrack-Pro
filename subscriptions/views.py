from django.shortcuts import render
from .models import PlanTier


def pricing_page(request):
    """
    Displays the different membership tiers available for purchase
    """
    plans = PlanTier.objects.filter(is_active=True).order_by('price')

    context = {
        'plans': plans,
    }
    return render(request, 'subscriptions/pricing.html', context)
