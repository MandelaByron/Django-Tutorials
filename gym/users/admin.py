from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', "first_name", "last_name", "is_staff", "public_id"]
    
    search_fields = ['email', "fist_name", "last_name"]
    
    fieldsets = (
        (
           (None, {"fields":("password",)})
           
        ),
        
        (
            ("Personal Info", {"fields":('first_name', 'last_name', 'email')})
        ),

        (
            ("Permissions", {"fields":('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')})
        
        ),
        
        (
            ("Important Dates", {"fields":("last_login", )})
        )
    )
    
    add_fieldsets =(
        
        (None, {
            'classes': ('wide',),
            'fields': ("first_name","last_name",'email', 'password1', 'password2'),
        }),
        
    )
    
    
    ordering = ['email']