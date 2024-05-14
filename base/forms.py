from django.forms import ModelForm
from allauth.account.forms import SignupForm
from .models import Room, Message, ConnectionString, Device #, UserIPAddress
from django import forms

from allauth.account.forms import SignupForm

class MyCustomSignupForm(SignupForm):
    # Add fields for first name and last name with placeholders
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='First Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your first name'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Last Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your last name'})
    )

    def save(self, request):
        # Call the parent class's save method to handle the standard save process
        user = super().save(request)
        
        # After the user is saved, update the first name and last name
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        # Save the user to apply the changes
        user.save()
        
        # Return the user object as required
        return user

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),  # Use Textarea for multiline input
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3}),
        }

# class UserIPAddressForm(forms.ModelForm):
#     class Meta:
#         model = UserIPAddress
#         fields = ['ip_address']
#         labels = {
#             'ip_address': 'IP Address',
#         }

class ConnectionStringForm(forms.ModelForm):
    class Meta:
        model = ConnectionString
        fields = ['connection_string']
        labels = {
            'primary_connection_string': 'Connection String'
        }

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['device_type', 'device_name']
        labels = {
            'device_type': 'Device Type',
            'device_name': 'Device Name'
        }