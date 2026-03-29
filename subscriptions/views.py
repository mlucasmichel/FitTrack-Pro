import stripe
import datetime
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        user_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')
        stripe_subscription_id = session.get('subscription')

        try:
            print(f"--- Processing Real Checkout for User ID: {user_id} ---")
            user = User.objects.get(id=user_id)

            stripe_sub = stripe.Subscription.retrieve(stripe_subscription_id)

            line_items = stripe.checkout.Session.list_line_items(session.id, limit=1)
            price_id = line_items.data[0].price.id
            print(f"Verified Price ID: {price_id}")

            plan_tier = PlanTier.objects.filter(stripe_price_id=price_id).first()

            raw_end = getattr(stripe_sub, 'current_period_end', None)
            if raw_end:
                period_end = timezone.make_aware(datetime.datetime.fromtimestamp(raw_end))
            else:
                period_end = timezone.now() + datetime.timedelta(days=30)

            subscription, created = Subscription.objects.update_or_create(
                user=user,
                defaults={
                    'plan_tier': plan_tier,
                    'stripe_customer_id': stripe_customer_id,
                    'stripe_subscription_id': stripe_subscription_id,
                    'status': 'active',
                    'current_period_end': period_end,
                }
            )
            print(f"✅ SUCCESS: {user.username} is now Premium!")
        except Exception as e:
            print(f"Error processing webhook: {e}")

    return HttpResponse(status=200)


@login_required
def create_portal_session(request):
    """
    Creates a Stripe Customer Portal session and redirects the user.
    This allows them to manage their subscription, payment methods, and billing history.
    """
    try:
        customer_id = request.user.subscription.stripe_customer_id
    except Exception:
        customer_id = None

    if not customer_id:
        messages.error(request, "You do not have an active subscription to manage.")
        return redirect('profile')

    try:
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=request.build_absolute_uri(reverse('profile')),
        )
        return redirect(session.url, code=303)
    except Exception as e:
        print(f"Stripe Portal Error: {e}")
        messages.error(request, "Unable to access the billing portal at this time.")
        return redirect('profile')
