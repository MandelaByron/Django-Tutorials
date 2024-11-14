from django.contrib import admin
from .models import Subscription, MembershipPlan, Payment

# Register your models here.

admin.site.register([Subscription, MembershipPlan, Payment])