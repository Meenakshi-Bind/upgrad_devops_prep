from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Vehicle, ParkingSession, ParkingLot

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered.')
        return email

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['license_plate', 'vehicle_type', 'make', 'model', 'color']
        widgets = {
            'license_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'make': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ParkingSessionForm(forms.ModelForm):
    class Meta:
        model = ParkingSession
        fields = ['vehicle', 'parking_lot']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'parking_lot': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(owner=user)
        self.fields['parking_lot'].queryset = ParkingLot.objects.filter(available_spaces__gt=0)
