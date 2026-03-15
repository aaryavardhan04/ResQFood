from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import User, FoodListing, NGO
from django.db.models import Q

def home(request):
    query = request.GET.get('pincode')
    listings = FoodListing.objects.filter(status='Available')
    if query:
        pincode_list = [p.strip() for p in query.split(',')]
        listings = listings.filter(pincode__in=pincode_list)
    return render(request, 'home.html', {'listings': listings})

def register_select(request):
    return render(request, 'register_select.html')

def register_ngo_org(request):
    if request.method == 'POST':
        # Tier 1: NGO is created but 'is_verified' defaults to False in models.py
        NGO.objects.create(
            name=request.POST['name'],
            ngo_id=request.POST['ngo_id'],
            address=request.POST['address'],
            pincode=request.POST['pincode'],
            security_code=request.POST['sec_code']
        )
        messages.success(request, "NGO Profile submitted! It will appear for volunteers once Admin verifies it.")
        return redirect('login')
    return render(request, 'register_ngo.html')

def register_form(request, role_type):
    if request.method == 'POST':
        data = request.POST
        is_active_ngo_vol = False
        
        # Tier 2 Logic: NGO Volunteer automated verification
        if role_type == 'ngo_volunteer':
            # Check ID, Security Code, AND Tier 1 status (Admin Verification)
            parent_ngo = NGO.objects.filter(
                ngo_id=data['ngo_id'], 
                security_code=data['sec_code'],
                is_verified=True  # NEW: Parent NGO must be verified by Admin
            ).first()
            
            if parent_ngo:
                is_active_ngo_vol = True
            else:
                messages.error(request, "Invalid credentials or NGO is not yet verified by Admin.")
                return redirect('register_form', role_type=role_type)

        try:
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                role=role_type.upper(),
                phone=data['phone'],
                address=data.get('address', ''),
                pincode=data['pincode'],
                is_verified_ngo=is_active_ngo_vol  # Automatically verified if Tier 1 passed
            )
            
            if role_type == 'restaurant':
                user.fssai_license = data['fssai']
            elif 'donor' in role_type or 'volunteer' in role_type:
                user.aadhaar_number = data.get('aadhaar')
                
            if role_type == 'ngo_volunteer':
                user.ngo_id = data['ngo_id']
            
            user.save()
            login(request, user)
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Error: {e}")
            
    return render(request, f'register_{role_type}.html')

# login_view, logout_view, dashboard remain same but logic is tighter
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.role in ['RESTAURANT', 'INDIVIDUAL_DONOR']:
        items = FoodListing.objects.filter(donor=request.user)
        return render(request, 'dashboard_donor.html', {'my_items': items})
    else:
        claims = FoodListing.objects.filter(claimed_by=request.user)
        return render(request, 'dashboard_volunteer.html', {'my_claims': claims})

def list_food(request):
    if request.method == 'POST':
        FoodListing.objects.create(
            donor=request.user,
            food_name=request.POST['food_name'],
            quantity=request.POST['quantity'],
            image=request.FILES['image'],
            preservation_required='preservation' in request.POST,
            pincode=request.POST['pincode']
        )
        return redirect('dashboard')
    return render(request, 'list_food.html')

def claim_food(request, food_id):
    food = get_object_or_404(FoodListing, id=food_id)
    user = request.user
    
    # Tier 2 Enforcement: NGO Volunteers must be verified via the parent NGO
    if user.role == 'NGO_VOLUNTEER' and not user.is_verified_ngo:
        messages.error(request, "Access Restricted: Your NGO is not yet verified by Admin.")
        return redirect('home')
    
    # Claiming logic
    if food.status == 'Available':
        food.status = 'Claimed'
        food.claimed_by = user
        food.generate_otp()
        messages.success(request, f"Claimed! Your OTP is {food.otp}")
    return redirect('dashboard')

def verify_otp(request, food_id):
    food = get_object_or_404(FoodListing, id=food_id)
    if request.method == 'POST':
        if food.otp == request.POST.get('otp'):
            food.status = 'Verified'
            food.save()
            messages.success(request, "Verification Successful!")
        else:
            messages.error(request, "Invalid OTP!")
    return redirect('dashboard')