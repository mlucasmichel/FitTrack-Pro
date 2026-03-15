from django.urls import path
from . import views

urlpatterns = [
    path('pricing/', views.pricing_page, name='pricing'),
    path('checkout/<int:plan_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('success/', views.payment_success, name='payment_success'), # Temporary path
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
