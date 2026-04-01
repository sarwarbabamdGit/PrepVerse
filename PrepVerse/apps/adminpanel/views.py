from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from core.models import TopicSearch, UserAttempt
from django.db.models import Count, Avg
import json

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_searches = TopicSearch.objects.count()
    
    # Most searched topics
    trending_topics = TopicSearch.objects.values('topic_name').annotate(count=Count('topic_name')).order_by('-count')[:10]
    
    # Data for charts
    trending_labels = [t['topic_name'] for t in trending_topics]
    trending_data = [t['count'] for t in trending_topics]
    
    # Active users
    active_users = User.objects.annotate(search_count=Count('searches')).order_by('-search_count')[:10]
    
    # Average score
    avg_score = UserAttempt.objects.aggregate(avg=Avg('score'))['avg'] or 0
    
    context = {
        'total_users': total_users,
        'total_searches': total_searches,
        'trending_labels': json.dumps(trending_labels),
        'trending_data': json.dumps(trending_data),
        'active_users': active_users,
        'avg_score': round(avg_score, 2)
    }
    return render(request, 'adminpanel/dashboard.html', context)

@user_passes_test(is_admin)
def user_management(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'adminpanel/users.html', {'users': users})

@user_passes_test(is_admin)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser: # Don't delete superadmins unless through django admin
        user.delete()
    return redirect('adminpanel:users')

@user_passes_test(is_admin)
def user_details(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    searches = TopicSearch.objects.filter(user=target_user)
    attempts = UserAttempt.objects.filter(user=target_user)
    return render(request, 'adminpanel/user_details.html', {
        'target_user': target_user,
        'searches': searches,
        'attempts': attempts
    })
