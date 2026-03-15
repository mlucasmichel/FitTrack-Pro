from django.contrib import admin
from .models import PlanTier, Subscription


@admin.register(PlanTier)
class PlanTierAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stripe_price_id', 'is_active')
    list_filter = ('is_active',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_tier', 'status', 'current_period_end')
    list_filter = ('status', 'plan_tier')
    search_fields = ('user__username', 'stripe_customer_id',
                     'stripe_subscription_id')
    readonly_fields = ('stripe_customer_id', 'stripe_subscription_id')
