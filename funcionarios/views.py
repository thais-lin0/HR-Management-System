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
from django.db import IntegrityError
import string
import random
from django.contrib.auth.forms import SetPasswordForm


def home(request):
    return render(request, 'home.html')


def sobre(request):
    return render(request, 'sobre.html')

def signup(request):

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
        return render(request, 'user_login.html', {'form': AuthenticationForm()})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is None:
            error_message = 'Usuário ou senha incorreto!'
            return render(request, 'user_login.html', {'form': AuthenticationForm(), 'error': error_message})

        if user.last_login is None:
            # First login, redirect to password reset page
            login(request, user)
            return redirect('reset_password')

        login(request, user)
        return redirect('home')

def make_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def reset_password(request):
    if request.method == 'GET':
        return render(request, 'reset_password.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        User = get_user_model()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, 'reset_password.html', {'error': 'Nome de usuário inválido'})

        if new_password != confirm_password:
            return render(request, 'reset_password.html', {'error': 'Senhas não conferem'})

        user.set_password(new_password)
        user.save()

        # Log in the user with the new password
        user = authenticate(request, username=username, password=new_password)
        if user is not None:
            login(request, user)

        return redirect('home')

def funcionarios(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        input_username = request.POST.get('username')
        role = request.POST.get('role')
        salary = request.POST.get('salary')
        work_section = request.POST.get('work_section')

        if name and role and salary and work_section and input_username:
            password = make_random_password()  # Generate a random password
            employee = Employee(name=name, role=role, salary=salary, work_section=work_section, username=input_username)
            employee.save()

            # Check if a user with the same username already exists
            User = get_user_model()
            try:
                User = User.objects.create_user(username=input_username, password=password)
                return render(request, 'sucesso.html', {'password': password, 'input_username': input_username})
            except IntegrityError:
                return render(request, 'user_exists.html', {'username': input_username})
            
        else:
            return render(request, 'fail.html')
    else:
        return render(request, 'funcionarios.html')


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

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
    employee = get_object_or_404(Employee, username=request.user.username)
    return render(request, 'dados.html', {'employee': employee})

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