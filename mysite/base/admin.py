from django.contrib import admin
from .models import Room, Message, ConnectionString, Device #, UserIPAddress
# Register your models here.
admin.site.register(Room)
admin.site.register(Message)
# admin.site.register(UserIPAddress)
admin.site.register(ConnectionString)
admin.site.register(Device)