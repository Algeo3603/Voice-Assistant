from django.urls import path
from . import views
# Suggested code may be subject to a license. Learn more: ~LicenseLog:1769590938.

urlpatterns = [
    path('', views.home, name="home"),
    path('logout/',views.logoutUser, name="logout"),
    path('chat-room/', views.chatRoom, name="chat-room"),
    path('control/', views.control, name="control-devices"),
    path('create-connection/', views.createConnection, name="create-connection"),
    path('update-connection/<int:pk>/', views.updateConnection, name="update-connection"),
    path('delete-connection/<int:pk>/', views.deleteConnection, name="delete-connection"),
    path('devices/', views.devices, name="devices"),
    path('device/<uuid:pk>/', views.device, name="device"),
    path('devices/create/', views.createDevice, name="create-device"),
    path('devices/update/<uuid:pk>/', views.updateDevice, name="update-device"),
    path('devices/delete/<uuid:pk>/', views.deleteDevice, name="delete-device"),
    path('sendmessage/<uuid:pk>/', views.sendMessage, name="send-message"),
    path('room/<uuid:pk>/', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<uuid:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<uuid:pk>/', views.deleteRoom, name="delete-room"),
]