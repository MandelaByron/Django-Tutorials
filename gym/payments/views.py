from django.shortcuts import render, get_object_or_404, redirect
from .models import MembershipPlan, Subscription, Payment
from django.utils import timezone
from django.conf import settings
import requests
from django.contrib.auth.decorators import login_required
from datetime import timedelta

def subscribe(request):
    plans = MembershipPlan.objects.all()
    return render(request, 'subscribe.html', {'title': 'Subscribe', 'plans': plans})

@login_required
def initiate_payment(request):
    if request.method == 'POST':
        plan_id = request.POST['plan_id']
        plan = get_object_or_404(MembershipPlan, id=plan_id)
        return render(request, 'payment_page.html', {
            'plan': plan,
            'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY
        })
    else:
        return render(request, 'payment_page.html')
    
@login_required
def verify_payment(request):
    reference = request.GET.get('reference')
    plan_id = request.GET.get('plan_id')
    
    # Verify payment with Paystack
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }
    response = requests.get(url, headers=headers)
    result = response.json()

    if result['status'] and result['data']['status'] == 'success':
        # Payment is successful
        plan = MembershipPlan.objects.get(id=plan_id)
        
        # Check for an existing active subscription
        active_subscription = Subscription.objects.filter(user=request.user, status='Active').first()
        
        if active_subscription:
            # Update the existing subscription
            active_subscription.plan = plan
            active_subscription.start_date = timezone.now()
            
            # Set the end date based on the plan type
            if plan.plan_type == 'M':
                active_subscription.end_date = active_subscription.start_date + timedelta(days=30)
            elif plan.plan_type == 'Q':
                active_subscription.end_date = active_subscription.start_date + timedelta(days=90)
            elif plan.plan_type == 'Y':
                active_subscription.end_date = active_subscription.start_date + timedelta(days=365)
            
            active_subscription.save()
        else:
            # Create a new subscription if none exists
            active_subscription = Subscription.objects.create(
                user=request.user,
                plan=plan,
                start_date=timezone.now(),
                status='Active',
                end_date=timezone.now() + timedelta(days={
                    'M': 30,
                    'Q': 90,
                    'Y': 365
                }[plan.plan_type])
            )

        # Record the payment
        Payment.objects.create(
            user=request.user,
            amount=plan.price,
            transaction_id=result['data']['reference'],
            status='Success',
            subscription=active_subscription
        )

        return redirect('profile')  # Redirect to profile page after successful payment
    else:
        return redirect('payment_failed')  # Redirect if payment fails