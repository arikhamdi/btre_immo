from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth.models import User, auth

from contacts.models import Contact


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('accounts:login')
    else:
        return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        # check if password match
        if password == password2:
            # check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return redirect('accounts:register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already being used')
                    return redirect('accounts:register')
                else:
                    # looks good
                    user = User.objects.create(
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        email=email)
                    # auth.login(request, user)
                    user.set_password(password)
                    user.save()
                    messages.success(
                        request, 'You are now registered and can log in')
                    return redirect('accounts:login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('accounts:register')
    else:
        return render(request, 'accounts/register.html')


def dashboard(request):
    user_contacts = Contact.objects.filter(
        user_id=request.user.id).order_by('-contact_date')
    context = {
        'user_contacts': user_contacts,
    }
    return render(request, 'accounts/dashboard.html', context)


def logout(request):
    auth.logout(request)
    messages.success(request, 'You are now logged out')
    return redirect('pages:index')
