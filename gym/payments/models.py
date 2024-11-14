from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

class MembershipPlan(models.Model):
    PLAN_CHOICES = [
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('Y', 'Yearly'),
    ]
    
    name = models.CharField(max_length=100)
    
    plan_type = models.CharField(max_length=1, choices=PLAN_CHOICES)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    description = models.TextField(blank=True)
    
    paystack_plan_code = models.CharField(max_length=100)
    

    
    def __str__(self):
        return f"{self.get_plan_type_display()} - {self.price}"



class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'Active'
        INACTIVE = 'Inactive'
        EXPIRED = 'Expired'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INACTIVE)


    def save(self, *args, **kwargs):
        # Check if this is a new subscription or if the plan has changed
        if not self.pk or Subscription.objects.get(pk=self.pk).plan != self.plan:
            # Recalculate the end date based on the new plan type
            if self.plan.plan_type == 'M':
                self.end_date = self.start_date + timedelta(days=30)
            elif self.plan.plan_type == 'Q':
                self.end_date = self.start_date + timedelta(days=90)
            elif self.plan.plan_type == 'Y':
                self.end_date = self.start_date + timedelta(days=365)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.email} - {self.plan.name}"

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')  # Example: Success, Failed, Pending

    def __str__(self):
        return f"{self.user.email} - {self.amount} - {self.status}"
