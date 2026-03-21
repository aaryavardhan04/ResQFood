from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, NGO, FoodListing

class CustomUserAdmin(UserAdmin):
    # This ensures your custom fields are visible when editing a user
    model = User
    list_display = ['username', 'email', 'role', 'pincode', 'is_verified_ngo']
    list_filter = ['role', 'is_verified_ngo', 'pincode']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined',)}),
        ('ResQFood Profile', {
            'fields': (
                'role', 'phone', 'pincode', 'address', 
                'fssai_license', 'aadhaar_number', 
                'ngo_id', 'is_verified_ngo'
            )
        }),
    )

class NGOAdmin(admin.ModelAdmin):
    # This is Tier 1 Verification: Approve the NGO here
    list_display = ['name', 'ngo_id', 'pincode', 'is_verified']
    list_filter = ['is_verified', 'pincode']
    search_fields = ['name', 'ngo_id']
    
    # NEW: Allows you to verify NGOs directly from the list view
    list_editable = ['is_verified'] 

class FoodListingAdmin(admin.ModelAdmin):
    list_display = ['food_name', 'donor', 'donor_name', 'address', 'pincode', 'status', 'get_claimed_by', 'upload_time', 'time_left']
    list_filter = ['status', 'pincode']
    search_fields = ['food_name', 'pincode']

    def get_claimed_by(self, obj):
        return obj.claimed_by.username if obj.claimed_by else "Not Claimed"
    get_claimed_by.short_description = "Claimed By"

# Registering models with their custom Admin classes
admin.site.register(User, CustomUserAdmin)
admin.site.register(NGO, NGOAdmin)
admin.site.register(FoodListing, FoodListingAdmin)