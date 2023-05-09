from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test



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
                if code == 'Admin123@':  # Replace with your staff code
                    user.is_staff = True
                else:
                    return render(request, 'signup.html', {'form': form, 'error': 'Invalid staff code'})
            user.save()
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

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def funcionarios(request):
    return render(request, 'funcionarios.html')

def ferias(request):
    return render(request, 'ferias.html')

@login_required
def staff_only_view(request):
    if request.user.is_staff:
        # code for staff-only view goes here
        return render(request, 'staffonly.html')
    else:
        # code for non-staff view goes here
        return render(request, 'nonstaff.html')