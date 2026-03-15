from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class PlanTier(models.Model):
    """
    Defines the different subscription plans available for purchase
    """
    name = models.CharField(max_length=100, help_text="e.g., Pro Monthly")
    description = models.TextField()
    price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    stripe_price_id = models.CharField(
        max_length=100, unique=True, help_text="The Price ID from Stripe Dashboard")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (${self.price})"


class Subscription(models.Model):
    """
    Links User to Subscription status
    """
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('past_due', 'Past Due'),
        ('unpaid', 'Unpaid'),
        ('incomplete', 'Incomplete'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    plan_tier = models.ForeignKey(
        PlanTier, on_delete=models.SET_NULL, null=True, blank=True)

    stripe_customer_id = models.CharField(
        max_length=100, blank=True, null=True)
    stripe_subscription_id = models.CharField(
        max_length=100, blank=True, null=True, unique=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='incomplete')

    current_period_end = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_status_display()}"

    @property
    def is_premium(self):
        """
        Check if the user has full access
        """
        return self.status == 'active'
