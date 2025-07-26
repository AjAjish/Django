from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/',views.login,name='login'),
    path('set_password/<uuid:user_id>/', views.set_password, name='set_password'),
    path('send_welcome_email/<uuid:user_id>/', views.send_welcome_email, name='send_welcome_email'),
    path('list_form_data/',views.list_form_data,name='list_form_data'),
    path('search_by_admin/', views.search_by_admin, name='search_by_admin'),
    path('search_by_user/', views.search_by_user, name='search_by_user'),
    path('logout/', views.logout, name='logout'),
    path('view_form_data/', views.view_form_data, name='view_form_data'),
    path('add_form_data/',views.add_form_data,name='add_form_data'),
    path('edit_form_data/<uuid:user_id>/', views.edit_form_data, name='edit_form_data'),
    path('delete_form_data/<uuid:user_id>/', views.delete_form_data, name='delete_form_data'),
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('profile_view/<uuid:user_id>/', views.profile_view, name='profile_view'),
    path('profile_logout/<uuid:user_id>/', views.profile_logout, name='profile_logout'),
    path('upload_profile_picture/<uuid:user_id>/', views.upload_profile_picture, name='upload_profile_picture'),
]