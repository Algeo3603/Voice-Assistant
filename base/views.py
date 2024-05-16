from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Room, Message, ConnectionString, Device
from .forms import RoomForm, MessageForm, ConnectionStringForm, DeviceForm
from .modules.llm import LLM
from .modules.iothub import message_to_raspberrypi
# Create your views here.


def home(request):
    return render(request, 'base/home.html')

@login_required(login_url='account_login')
def chatRoom(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    if q:
        rooms = Room.objects.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q)
        )
        room_messages = Message.objects.filter(
            room__in=rooms
        )
    else:
        rooms = Room.objects.all()
        room_messages = Message.objects.all()

    room_count = rooms.count()

    context = {
        'rooms': rooms,
        'room_count': room_count,
        'room_messages': room_messages,
    }
    return render(request, 'base/chat_room.html', context)

def room(request, pk):
    llm_demo = LLM()
    # room = Room.objects.get(id=pk)
    room = get_object_or_404(Room, id=pk)
    room_messages = room.messages.all()
    message_form = MessageForm()
    bot_message_form = MessageForm()
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.user = request.user
            message.room = room
            message.sender = 'User'
            message.save()

            bot_reply = llm_demo.AI(message.message)
            if bot_reply:
                bot_message = bot_message_form.save(commit=False)
                bot_message.user = None
                bot_message.room = room
                bot_message.sender = 'Assistant'
                bot_message.message = bot_reply
                bot_message.save()

            return redirect('room', pk=pk)

    context = {'room': room, 'room_messages': room_messages, 'message_form': message_form, 'bot_message_form': bot_message_form}
    return render(request, 'base/room.html', context)

@login_required(login_url='account_login')
def createRoom(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect('chat-room')  # Replace 'chat-room' with your actual URL name
    else:
        form = RoomForm()

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='account_login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('chat-room')
        
    context = {'form': form, 'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='account_login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here!!")
    
    if request.method == 'POST':
        room.delete()
        return redirect('chat-room')
    
    context = {'obj': room}
    return render(request, 'base/delete_room.html', context)

@login_required(login_url='account_login')
def createConnection(request):
    if request.method == 'POST':
        form = ConnectionStringForm(request.POST)
        if form.is_valid():
            connection_string = form.save(commit=False)
            connection_string.user = request.user  # Assign the current user to the connection string
            connection_string.save()  # Save the object to the database
            messages.success(request, 'Connection string added successfully.')
            return redirect('control-devices')  # Redirect to a page that lists all connection strings
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ConnectionStringForm()

    context = {'form': form}
    return render(request, 'base/connection_form.html', context)

@login_required(login_url='account_login')
def updateConnection(request, pk):
    connection_string = ConnectionString.objects.get(id=pk)

    if request.user != connection_string.user:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        form = ConnectionStringForm(request.POST, instance=connection_string)
        if form.is_valid():
            form.save()
            return redirect('control-devices')
    else:
        form = ConnectionStringForm(instance=connection_string)

    context = {'form': form, 'connection_string': connection_string}
    return render(request, 'base/connection_form.html', context)

@login_required(login_url='account_login')
def deleteConnection(request, pk):
    connection_string = ConnectionString.objects.get(id=pk)

    if request.user != connection_string.user:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        connection_string.delete()
        return redirect('control-devices')

    context = {'connection_string': connection_string}
    return render(request, 'base/delete_connection.html', context)

@login_required(login_url='account_login')
def control(request):
    connection_string = ConnectionString.objects.filter(user=request.user).first()
    # print(connection_string, "string", connection_string.connection_string)
    if connection_string:
        context = {'connection_strings': connection_string}
        return render(request, 'base/control.html', context)
    else:
        return redirect('create-connection')

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='account_login')
def devices(request):
    devices = Device.objects.filter(user=request.user)
    if devices:
        context = {'devices': devices}
        return render(request, 'base/devices.html', context)
    else:
        return redirect('create-device')

def device(request, pk):
    device = Device.objects.get(id=pk)
    context = {'device': device}
    # print(device, type(device))
    return render(request, 'base/device.html', context)

@login_required(login_url='account_login')
def sendMessage(request, pk):
    # Get the device based on pk and user
    device = Device.objects.filter(pk=pk, user=request.user).first()
    device_name = device.device_name
    device_status = device.status
    device_connection_string = str(device.connection_string)
    print(device_connection_string, type(device_connection_string), str(device_connection_string))
    if not device:
        # Device not found or does not belong to the user
        messages.error(request, 'Device not found or you do not have permission to access it.')
        # return JsonResponse({'error': 'Device not found or unauthorized'}, status=404)
        
    try:
        message_sent = message_to_raspberrypi(device_name, device_connection_string, device_status)
        if message_sent:
            messages.success(request, 'Message sent successfully to IoT Hub.')
            device.status = not device.status
            device.save()
        else:
            messages.error(request, 'Failed to send message to IoT Hub.')
            print("failed message")
    except Exception as e:
        messages.error(request, f'Error sending message to IoT Hub: {e}')
        print("error")

    context = {'device': device}
    return render(request, 'base/device.html', context)

@login_required(login_url='account_login')
def createDevice(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            device = form.save(commit=False)
            device.user = request.user
            device.connection_string = ConnectionString.objects.filter(user=request.user).first()
            device.save()
            return redirect('devices')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = DeviceForm()

    context = {'form': form}
    return render(request, 'base/device_form.html', context)

@login_required(login_url='account_login')
def updateDevice(request, pk):
    device = Device.objects.get(id=pk)
    if request.user != device.user:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('devices')
    else:
        form = DeviceForm(instance=device)

    context = {'form': form, 'device': device}
    return render(request, 'base/device_form.html', context)

@login_required(login_url='account_login')
def deleteDevice(request, pk):
    device = Device.objects.get(id=pk)
    if request.user != device.user:
        return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        device.delete()
        return redirect('devices')

    context = {'device': device}
    return render(request, 'base/delete_device.html', context)
    