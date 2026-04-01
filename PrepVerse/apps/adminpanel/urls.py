from django.urls import path
from . import views, admin_actions

app_name = 'adminpanel'

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='dashboard'),
    path('users/', views.user_management, name='users'),
    path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
    path('users/details/<int:user_id>/', views.user_details, name='user_details'),
    path('users/create-admin/', admin_actions.create_admin, name='create_admin'),
]
