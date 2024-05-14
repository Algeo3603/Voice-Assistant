from django.db import models
from django.conf import settings
import uuid
# Create your models here.

class Room(models.Model):
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hosted_rooms')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10)  # 'User' or 'Bot'
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(auto_now=True)

    # class Meta:
    #     ordering = ['-updated', '-timestamp']

    def __str__(self):
        return f"{self.sender} - {self.timestamp} - {self.message[:50]}"
    
# class UserIPAddress(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     ip_address = models.CharField(max_length=45)  # Assuming IPv4 or IPv6 address

#     def __str__(self):
#         return f"IP Address: {self.ip_address} - User: {self.user.email}"

class ConnectionString(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    connection_string = models.CharField(max_length=255, unique = True)

    def __str__(self):
        return f"Connection String: {self.connection_string} - User: {self.user.email}"


class Device(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # device_id = models.CharField(max_length=255, unique=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    connection_string = models.ForeignKey(ConnectionString, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=255)
    device_name = models.CharField(max_length=255, unique = True)
    status = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Device Type: {self.device_type} - Device Name: {self.device_name} - Status: {self.status} - User: {self.user.email}"