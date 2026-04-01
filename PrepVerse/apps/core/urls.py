from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('search/', views.search_topic, name='search'),
    path('submit-test/<int:topic_id>/', views.submit_test, name='submit_test'),
    path('history/', views.history_view, name='history'),
    path('history/delete/<int:topic_id>/', views.delete_history, name='delete_history'),
    path('bookmark/toggle/<int:topic_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('profile/', views.profile_view, name='profile'),
]
