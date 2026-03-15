import stripe
from django.shortcuts import render
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Subscription, PlanTier
from django.contrib.auth import get_user_model


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


# Stripe webhook to handle subscription events
User = get_user_model()


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers.get('STRIPE_SIGNATURE')
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Pull data we passed earlier in create_checkout_session
        user_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        # Get the User and update/create their Subscription record
        try:
            user = User.objects.get(id=user_id)
            # Fetch the subscription from Stripe to get the period end date
            stripe_sub = stripe.Subscription.retrieve(stripe_subscription_id)

            subscription, created = Subscription.objects.update_or_create(
                user=user,
                defaults={
                    'stripe_customer_id': stripe_customer_id,
                    'stripe_subscription_id': stripe_subscription_id,
                    'status': 'active',
                    'current_period_end': timezone.datetime.fromtimestamp(stripe_sub.current_period_end, tz=timezone.utc),
                }
            )
            print(f"✅ Subscription for user {user.username} activated!")
        except User.DoesNotExist:
            print("❌ User not found during webhook processing")

    return HttpResponse(status=200)
