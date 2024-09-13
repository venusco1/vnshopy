from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # List the fields you want to display in the user list view
    list_display = ['username', 'mb_number_or_email'] 

    # Define the fields you want to use for the user creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'mb_number_or_email', 'password1', 'password2'),
        }),
    )

    # Define the fields you want to use for the user change form
    fieldsets = (
        (None, {'fields': ('username', 'mb_number_or_email', 'password')}),
    )
    
    # Required for handling user creation
    filter_horizontal = ()
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)
