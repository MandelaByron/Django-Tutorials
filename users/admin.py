from django.contrib import admin
from .models import Users
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(Users)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', "first_name", "last_name", "is_staff", "public_id"]
    
    search_fields = ['email', "fist_name", "last_name"]
    
    ordering = ['email']
    
    fieldsets = (
        (
           (None, {"fields":("password",)})
           
        ),
        
        (
            ("Personal Info", {"fields":('first_name', 'last_name', 'email', "age", "avatar")})
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
            'fields': ("first_name","last_name",'email','age', 'password1', 'password2'),
        }),
        
    )