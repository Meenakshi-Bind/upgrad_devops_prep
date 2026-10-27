from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import ParkingLot, Vehicle, ParkingSession
from .forms import VehicleForm, ParkingSessionForm, UserRegistrationForm
from django.utils import timezone
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
# API 1: HTML → PDF
@csrf_exempt
def generate_pdf(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            response = requests.post(
                "https://rz27c392l4.execute-api.us-east-1.amazonaws.com/html/pdf",
                json=data
            )

            return JsonResponse({
                "status": "success",
                "api_response": response.json()
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


# API 2: Check API
@csrf_exempt
def check_api(request):
    if request.method == "GET":
        try:
            response = requests.get(
                "https://aljoyd5gl3.execute-api.us-east-1.amazonaws.com/check"
            )

            return JsonResponse({
                "status": "success",
                "api_response": response.json()
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')
import requests

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data.get('password1')

            try:
                # Call your Lambda API
                response = requests.post(
                    "https://aljoyd5gl3.execute-api.us-east-1.amazonaws.com/check",
                    json={"password": password}
                )

                result = response.json()

                strength = result.get("strength")
                score = result.get("score")

                #  Apply your own rule
                if score < 3:
                    messages.error(request, f"Password too weak: {strength}")
                    return render(request, 'register.html', {'form': form})

            except Exception as e:
                messages.error(request, f"Password API error: {str(e)}")
                return render(request, 'register.html', {'form': form})

            # If strong enough → save user
            user = form.save()
            login(request, user)
            messages.success(request, f'Registration successful! Password strength: {strength}')
            return redirect('dashboard')

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})
# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, 'Registration successful!')
#             return redirect('dashboard')
#     else:
#         form = UserRegistrationForm()
    
#     return render(request, 'register.html', {'form': form})

@login_required
def dashboard(request):
    user_vehicles = Vehicle.objects.filter(owner=request.user)
    active_sessions = ParkingSession.objects.filter(
        vehicle__owner=request.user,
        status='ACTIVE'
    )
    parking_lots = ParkingLot.objects.all()
    
    context = {
        'vehicles': user_vehicles,
        'active_sessions': active_sessions,
        'parking_lots': parking_lots,
    }
    return render(request, 'dashboard.html', context)

@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(owner=request.user)
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})

@login_required
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user
            vehicle.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    
    return render(request, 'vehicle_form.html', {'form': form})

@login_required
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vehicle updated successfully!')
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    
    return render(request, 'vehicle_form.html', {'form': form})

@login_required
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk, owner=request.user)
    
    if request.method == 'POST':
        # Prepare data BEFORE deleting
        data = {
    "license_plate": getattr(vehicle, 'license_plate', ''),
    "vehicle_number": getattr(vehicle, 'vehicle_number', ''),
    "make_model": getattr(vehicle, 'make_model', ''),
    "color": getattr(vehicle, 'color', '')
}

        try:
            # Call PDF API
            response = requests.post(
                "https://rz27c392l4.execute-api.us-east-1.amazonaws.com/html/pdf",
                json=data
            )

            # If API returns PDF file directly
            if response.headers.get('Content-Type') == 'application/pdf':
                pdf_response = HttpResponse(response.content, content_type='application/pdf')
                pdf_response['Content-Disposition'] = 'attachment; filename="receipt.pdf"'

                # Delete after generating PDF
                vehicle.delete()

                return pdf_response

            # If API returns JSON instead
            pdf_data = response.json()

        except Exception as e:
            messages.error(request, f"PDF generation failed: {str(e)}")
            return redirect('vehicle_list')

        # Delete vehicle
        vehicle.delete()

        messages.success(request, 'Vehicle deleted and PDF generated!')
        return redirect('vehicle_list')
    
    return render(request, 'vehicle_confirm_delete.html', {'vehicle': vehicle})
@login_required
def parking_lot_list(request):
    lots = ParkingLot.objects.all()
    return render(request, 'parking_lot_list.html', {'lots': lots})

@login_required
def start_parking(request):
    if request.method == 'POST':
        form = ParkingSessionForm(request.user, request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            parking_lot = session.parking_lot
            
            if parking_lot.available_spaces > 0:
                parking_lot.available_spaces -= 1
                parking_lot.save()
                session.save()
                messages.success(request, 'Parking session started!')
                return redirect('dashboard')
            else:
                messages.error(request, 'No available spaces in this parking lot')
    else:
        form = ParkingSessionForm(request.user)
    
    return render(request, 'start_parking.html', {'form': form})

@login_required
def end_parking(request, pk):
    session = get_object_or_404(ParkingSession, pk=pk, vehicle__owner=request.user, status='ACTIVE')
    
    if request.method == 'POST':
        session.check_out_time = timezone.now()
        session.status = 'COMPLETED'
        session.total_cost = session.calculate_cost()
        session.save()
        
        parking_lot = session.parking_lot
        parking_lot.available_spaces += 1
        parking_lot.save()
        
        messages.success(request, f'Parking session ended. Total cost: ${session.total_cost}')
        return redirect('dashboard')
    
    return render(request, 'end_parking.html', {'session': session})



@login_required
def parking_history(request):
    sessions = ParkingSession.objects.filter(
        vehicle__owner=request.user
    ).order_by('-check_in_time')
    
    return render(request, 'parking_history.html', {'sessions': sessions})