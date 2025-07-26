from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from .models import FormData,FormDataDetails

def home(request): 
    if request.method == 'GET':
        return render(request, 'home.html')

def add_form_data(request):
    if request.method == 'POST':
        # POST method is used for form submission and data creation.
        first_name = request.POST.get('first_name')
        if not first_name:
            return render(request, 'form.html', {'first_name_error': 'First name is required.'})
        last_name = request.POST.get('last_name')
        if not last_name:
            last_name = '-'
        email = request.POST.get('email')
        if not email:
            return render(request, 'form.html', {'email_error': 'Email is required.'})
        phone_no = request.POST.get('phone_no')
        if not phone_no:
            return render(request, 'form.html', {'ph_no_error': 'Phone number is required.'})
        address = request.POST.get('address')
        if not address:
            address = '-'
        
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
        if not user.first_name:
            return render(request, 'edit_form_data.html', {'user': user, 'first_name_error': 'First name is required.'})
        user.last_name = request.POST.get('last_name')
        if not user.last_name:
            user.last_name = '-'
        user.email = request.POST.get('email')
        if not user.email:
            return render(request, 'edit_form_data.html', {'user': user, 'email_error': 'Email is required.'})
        user.phone_no = request.POST.get('phone_no')
        if not user.phone_no:
            return render(request, 'edit_form_data.html', {'user': user, 'ph_no_error': 'Phone number is required.'})
        user.address = request.POST.get('address')
        if not user.address:
            user.address = '-'

        if FormData.objects.filter(phone_no=user.phone_no).exclude(user_id=user.user_id).exists():
            return render(request, 'edit_form_data.html', {'user': user, 'ph_no_error': 'Phone number already exists.'})
        if FormData.objects.filter(email=user.email).exclude(user_id=user.user_id).exists():
            return render(request, 'edit_form_data.html', {'user': user, 'email_error': 'Email already exists.'})
        
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
        if not first_name:
            return render(request, 'register.html', {'first_name_error': 'First name is required.'})
        last_name = request.POST.get('last_name')
        if not last_name:
            last_name = '-'
        email = request.POST.get('email')
        if not email:
            return render(request, 'register.html', {'email_error': 'Email is required.'})
        phone_no = request.POST.get('phone_no')
        if not phone_no :
            return render(request, 'register.html', {'ph_no_error': 'Phone number is required.'})
        address = request.POST.get('address')
        if not address:
            address = '-'

        if FormData.objects.filter(phone_no=phone_no).exists():
            return render(request, 'register.html', {'ph_no_error': 'Phone number already exists.'})
        if FormData.objects.filter(email=email).exists():
            return render(request, 'register.html', {'email_error': 'Email already exists.'})
        
        if first_name and email and phone_no:
            user = FormData.objects.create(first_name=first_name, last_name=last_name, email=email, phone_no=phone_no, address=address)
            messages.success(request, 'Registration successful. Check your email for set pawwsoed.')
            send_welcome_email(request, user.user_id)
            return redirect('home')
    return render(request, 'register.html')

def logout(request):
    messages.success(request, 'Logged out successfully.')
    return redirect('home')

def profile_logout(request, user_id):
    if FormData.objects.filter(user_id=user_id,role='admin').exists():
        messages.success(request, 'Logged out successfully.')
        return redirect('list_form_data')
    if FormData.objects.filter(user_id=user_id,role='user').exists():
        messages.success(request, 'Logged out successfully.')
        return redirect('view_form_data')

def search_by_admin(request):
    if request.method == 'POST':
        search_email = request.POST.get('search_email', '')
        users = FormData.objects.all().filter(email__icontains=search_email).values()
        return render(request, 'list_form_data.html', {'users': users})
    return render(request, 'list_form_data.html', {'users': FormData.objects.all()})

def search_by_user(request):
    if request.method == 'POST':
        search_email = request.POST.get('search_email', '')
        users = FormData.objects.all().filter(email__icontains=search_email).values().exclude(role='admin')
        return render(request, 'view_form_data.html', {'users': users})
    return render(request, 'view_form_data.html', {'users': FormData.objects.all().exclude(role='admin')})

def set_password(request, user_id):
    user = get_object_or_404(FormData, user_id=user_id)
    if request.method == 'POST':
        password = request.POST.get('password')
        if not password:
            return render(request, 'set_password.html', {'user': user, 'password_error': 'Password is required.'})
        confirm_password = request.POST.get('confirm_password')
        if not confirm_password:
            return render(request, 'set_password.html', {'user': user, 'password_error': 'Confirm password is required.'})
        if password != confirm_password:
            return render(request, 'set_password.html', {'user': user, 'password_error': 'Passwords do not match.'})
        user.password = password
        user.save()
        messages.success(request, 'Password set successfully. Please log in.')
        return redirect('login')
    return render(request, 'set_password.html', {'user': user})


def send_welcome_email(request, user_id):
    user = FormData.objects.get(user_id=user_id)
    # Construct the URL for the "Set Password" button
    set_password_url = request.build_absolute_uri(reverse('set_password', args=[user_id]))

    subject = "Set Password"
    message = f"""
    <html>
        <body>
            <p>Welcome to our website, {user.first_name}!</p>
            <p>You can set your password by clicking the button below:</p>
            <a href="{set_password_url}" style="background-color: #4CAF50; color: white; padding: 10px 15px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; font-size: 16px;">
                Set Password
            </a>
        </body>
    </html>
    """

    # Send the email
    send_mail(
        subject,
        '',
        'helloffyt100@gmail.com',  # From Email Address
        [user.email],                # Recipient Email
        fail_silently=False,
        html_message=message,        # HTML Email Body
    )
    
    return HttpResponse('Welcome email sent!')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            return render(request, 'forgot_password.html', {'email_error': 'Email is required.'})
        try:
            user = FormData.objects.get(email=email)
            send_forgot_password_email(request, user.user_id)
            messages.success(request, 'Check your email to reset your password.')
            return redirect('login')
        except FormData.DoesNotExist:
            return render(request, 'forgot_password.html', {'email_error': 'Email does not exist.'})
    
    return render(request, 'forgot_password.html')

def send_forgot_password_email(request,user_id):
    user = FormData.objects.get(user_id=user_id)
    set_password_url = request.build_absolute_uri(reverse('set_password', args=[user_id]))

    subject = "Reset Password"
    message = f"""
    <html>
        <body>
            <p>Hi {user.first_name},</p>
            <p>Click the button below to reset your password:</p>
            <a href="{set_password_url}" style="background-color: #4CAF50; color: white; padding: 10px 15px; text-align: center; text-decoration: none; display: inline-block; border-radius: 5px; font-size: 16px;">
                Reset Password
            </a>
        </body>
    </html>
    """

    send_mail(
        subject,
        '',
        'helloffyt100@gmail.com',
        [user.email],
        fail_silently=False,
        html_message=message,
    )
    return HttpResponse('Forgot password email sent!')

def profile_view(request,user_id):
    user = FormData.objects.get(user_id=user_id)
    return render(request, 'profile_view.html', {'user': user})
