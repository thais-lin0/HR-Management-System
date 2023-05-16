from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import TimeEntry, Employee, Ferias
from datetime import timedelta




def home(request):
    return render(request, 'home.html')


def sobre(request):
    return render(request, 'sobre.html')

def signup(request):
    User = get_user_model()  # Retrieve the User model dynamically

    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm()})
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            is_staff = request.POST.get('is_staff', False)
            if is_staff:
                code = request.POST.get('code', '')
                if code == 'Admin123@':
                    user.is_staff = True
                else:
                    return render(request, 'signup.html', {'form': form, 'error': 'Invalid staff code'})
            user.save()  # Save the user first to generate an id
            if is_staff:
                staff_group = Group.objects.get(name='staff')
                user.groups.add(staff_group)
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'GET':
        return render(request, 'user_login.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'user_login.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('home')

def add_employee(request):
    if request.method == 'POST':
        form = (request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        return render(request, 'fail.html', {'form': form})


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def funcionarios(request):
    return render(request, 'funcionarios.html')

@login_required
def staff_only_view(request):
    if request.user.is_staff:
        # code for staff-only view goes here
        return render(request, 'staffonly.html')
    else:
        # code for non-staff view goes here
        return render(request, 'nonstaff.html')


@login_required
def ponto(request):
    user = request.user
    today = timezone.localdate()
    time_entries = TimeEntry.objects.filter(user=user, start_time__date=today)

    if time_entries.exists():
        return render(request, 'ponto.html', {'already_punched': True})

    if request.method == 'POST':
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']

        TimeEntry.objects.create(user=user, start_time=start_time, end_time=end_time)
        return redirect('home')  # Replace 'home' with the URL of your desired page

    return render(request, 'ponto.html', {'already_punched': False})

@login_required
def ferias(request):
    user = request.user

    # Check if 30 days have passed since the latest requisition
    thirty_days_ago = timezone.now() - timedelta(days=30)
    latest_requisition = Ferias.objects.filter(user=user).order_by('-id').first()
    if latest_requisition and latest_requisition.created_at >= thirty_days_ago:
        status_message = get_status_message(latest_requisition.status)
        return render(request, 'status.html', {'status_message': status_message})

    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        reason = request.POST['reason']

        Ferias.objects.create(user=user, start_date=start_date, end_date=end_date, reason=reason)
        return redirect('status')

    return render(request, 'ferias.html')

@login_required
def status(request):
    user = request.user
    requisitions = Ferias.objects.filter(user=user).order_by('-id')

    if requisitions.exists():
        latest_requisition = requisitions.first()
        status_message = get_status_message(latest_requisition.status)
    else:
        status_message = "No requisition found."

    return render(request, 'status.html', {'status_message': status_message})

@login_required
def dados(request):
    try:
        employee = Employee.objects.get(name=request.user.username)
        return render(request, 'dados.html', {'employee': employee})
    except Employee.DoesNotExist:
        return render(request, '404.html')

@login_required
def aceiteferias(request):
    if not request.user.is_staff:
        # Only staff members can access this view
        return redirect('home')  # Replace 'home' with the URL of your desired page

    requisitions = Ferias.objects.all()

    if request.method == 'POST':
        requisition_id = request.POST.get('requisition_id')
        status = request.POST.get('status')

        requisition = get_object_or_404(Ferias, pk=requisition_id)
        requisition.status = status
        requisition.save()

    return render(request, 'aceiteferias.html', {'requisitions': requisitions})

def get_status_message(status):
    if status == 'Pending':
        return "Sua requisição está aguardando aprovação."
    elif status == 'Approved':
        return "Sua requisição foi aceita com sucesso. O RH entrará em contato para mais detalhes."
    elif status == 'Denied':
        return "Sua requisição foi negada. O RH entrará em contato para mais detalhes."
    else:
        return "Status desconhecido."