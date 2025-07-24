from django.shortcuts import render,redirect
from django.contrib import messages
from .models import FormData

def home(request): 
    if request.method == 'GET':
        return render(request, 'home.html')

def add_form_data(request):
    if request.method == 'POST':
        # POST method is used for form submission and data creation.
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')
        
        if FormData.objects.filter(phone_no=phone_no).exists():
            return render(request, 'form.html', {'ph_no_error' : 'Phone number already exists.'})

        if FormData.objects.filter(email=email).exists():
            return render(request, 'form.html', {'email_error' : 'Email already exists.'})

        FormData.objects.create(first_name=first_name,last_name=last_name,email=email,phone_no=phone_no,address=address)
        messages.success(request, 'Form data added successfully.')
        return redirect('list_form_data')

    return render(request,'form.html')

def list_form_data(request):
    if request.method == "GET":
        users = FormData.objects.all()
        return render(request, 'list_form_data.html', {'users': users})
    return render(request, 'list_form_data.html')

def edit_form_data(request, user_id):
    try:
        user = FormData.objects.get(user_id=user_id)
    except FormData.DoesNotExist:
        return render(request, 'edit_form_data.html', {'error': 'User not found.'})
    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone_no = request.POST.get('phone_no')
        user.address = request.POST.get('address')
        if FormData.objects.filter(phone_no=user.phone_no).exclude(user_id=user.user_id).exists():
            return render(request, 'edit_form_data.html', {'user': user, 'ph_no_error': 'Phone number already exists.'})
        if FormData.objects.filter(email=user.email).exclude(user_id=user.user_id).exists():
            return render(request, 'edit_form_data.html', {'user': user, 'email_error': 'Email already exists.'})
        print(user.first_name, user.last_name, user.email, user.phone_no, user.address)
        user.save()
        messages.success(request, 'Form data updated successfully.')
        return redirect('list_form_data')
    return render(request, 'edit_form_data.html', {'user': user})

def delete_form_data(request, user_id):
    user = FormData.objects.get(user_id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Form data deleted successfully.')
        return redirect('list_form_data')
    return render(request, 'delete_form_data.html', {'user': user})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email == 'ajish@gmail.com' and password == 'admin@123':
            return redirect('list_form_data')
        elif FormData.objects.filter(email=email, password=password).exists():
            print(f"User {email} logged in successfully.")
            return redirect('view_form_data')
        else:
            messages.error(request, 'Invalid email or password.')
    return render(request, 'login.html')

def view_form_data(request):
    if request.method == "GET":
        users = FormData.objects.all().exclude(role='admin')
        return render(request, 'view_form_data.html', {'users': users})
    return render(request, 'view_form_data.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_no = request.POST.get('phone_no')
        address = request.POST.get('address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'register.html', {'password_error': 'Passwords do not match.'})

        if FormData.objects.filter(phone_no=phone_no).exists():
            return render(request, 'register.html', {'ph_no_error': 'Phone number already exists.'})

        if FormData.objects.filter(email=email).exists():
            return render(request, 'register.html', {'email_error': 'Email already exists.'})

        FormData.objects.create(first_name=first_name, last_name=last_name, email=email, phone_no=phone_no, address=address, password=password)
        messages.success(request, 'Registration successful. Please log in.')
        return redirect('login')

    return render(request, 'register.html')

def logout(request):
    return redirect('home')

def search(request):
    if request.method == 'POST':
        search_email = request.POST.get('search_email', '')
        users = FormData.objects.all().filter(email__icontains=search_email).values()
        return render(request, 'list_form_data.html', {'users': users})
    return render(request, 'list_form_data.html', {'users': FormData.objects.all()})
