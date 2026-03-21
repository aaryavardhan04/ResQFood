from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_select, name='register_select'),
    path('register/ngo-org/', views.register_ngo_org, name='register_ngo_org'),
    path('register/<str:role_type>/', views.register_form, name='register_form'),
    path('list-food/', views.list_food, name='list_food'),
    path('claim-food/<int:food_id>/', views.claim_food, name='claim_food'),
    path('verify-otp/<int:food_id>/', views.verify_otp, name='verify_otp'),
    path('cancel-claim/<int:food_id>/', views.cancel_claim, name='cancel_claim'),
    path('delete-listing/<int:food_id>/', views.delete_listing, name='delete_listing'),
    path('dashboard/', views.dashboard, name='dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)