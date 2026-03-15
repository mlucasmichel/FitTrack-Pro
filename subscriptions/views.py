import stripe
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
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


# Set Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, plan_id):
    """
    Creates a Stripe Checkout Session for a specific subscription plan.
    """
    plan = get_object_or_404(PlanTier, id=plan_id)
    domain_url = request.build_absolute_uri('/')[:-1]

    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=request.user.id if request.user.is_authenticated else None,
            customer_email=request.user.email if request.user.is_authenticated else None,
            payment_method_types=['card'],
            mode='subscription',
            line_items=[
                {
                    'price': plan.stripe_price_id,
                    'quantity': 1,
                }
            ],
            success_url=domain_url +
            reverse('payment_success') + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=domain_url + reverse('pricing'),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        print(f"Stripe Error: {e}")
        return redirect('pricing')


# View to handle successful payment
def payment_success(request):
    return render(request, 'subscriptions/success.html')
