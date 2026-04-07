from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import TopicSearch, MCQ, UserAttempt, Bookmark
from .services import get_study_material_and_mcqs, get_youtube_videos
import json

@login_required
def dashboard(request):
    # Bookmarks
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('topic')
    # Recent Search History
    history = TopicSearch.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'bookmarks': bookmarks,
        'history': history,
        'username': request.user.username
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def search_topic(request):
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        if not topic_name:
            return redirect('core:dashboard')
        
        # Save search (even if it fails later)
        search_obj = TopicSearch.objects.create(user=request.user, topic_name=topic_name)
        
        # API Calls
        api_data = get_study_material_and_mcqs(topic_name)
        videos = get_youtube_videos(topic_name)
        
        if api_data:
            if 'error' in api_data:
                # Handle blocked content
                search_obj.study_material = f"ERROR: {api_data['error']}"
                search_obj.save()
            else:
                search_obj.study_material = api_data.get('study_material')
                search_obj.exam_pattern = api_data.get('exam_pattern')
                search_obj.previous_papers = api_data.get('previous_papers')
                search_obj.preparation_guidance = api_data.get('preparation_guidance')
                search_obj.save()
                
                # Save MCQs
                for q in api_data.get('mcqs', []):
                    options = q.get('options', [])
                    if len(options) >= 4:
                        MCQ.objects.create(
                            topic=search_obj,
                            question=q.get('question', 'N/A'),
                            option1=options[0],
                            option2=options[1],
                            option3=options[2],
                            option4=options[3],
                            correct_answer=q.get('correct_answer', 'A'),
                            explanation=q.get('explanation', '')
                        )
        
        return render(request, 'core/search_results.html', {
            'topic': search_obj,
            'videos': videos,
            'mcqs': search_obj.mcqs.all()
        })
    return redirect('core:dashboard')

@login_required
def submit_test(request, topic_id):
    if request.method == 'POST':
        topic = get_object_or_404(TopicSearch, id=topic_id)
        mcqs = topic.mcqs.all()
        score = 0
        total = mcqs.count()
        results = []
        
        # Answers are in POST data like 'ans_1': 'A', 'ans_2': 'B'...
        for idx, mcq in enumerate(mcqs, start=1):
            user_ans = request.POST.get(f'ans_{mcq.id}')
            correct = (user_ans == mcq.correct_answer)
            if correct:
                score += 1
            
            results.append({
                'mcq': mcq,
                'user_ans': user_ans,
                'is_correct': correct
            })
            
        # Save Attempt
        UserAttempt.objects.create(
            user=request.user,
            topic=topic,
            score=score,
            total_questions=total
        )
        
        # Fetch videos for results page too
        videos = get_youtube_videos(topic.topic_name)
        
        return render(request, 'core/test_results.html', {
            'topic': topic,
            'score': score,
            'total': total,
            'results': results,
            'videos': videos
        })
    return redirect('core:dashboard')

@login_required
def history_view(request):
    history = TopicSearch.objects.filter(user=request.user).order_by('-created_at')
    # For each history item, get its last score if available
    for item in history:
        last_attempt = UserAttempt.objects.filter(user=request.user, topic=item).order_by('-attempted_at').first()
        item.last_score = f"{last_attempt.score}/{last_attempt.total_questions}" if last_attempt else "N/A"
    
    return render(request, 'core/history.html', {'history': history})

@login_required
def delete_history(request, topic_id):
    topic = get_object_or_404(TopicSearch, id=topic_id, user=request.user)
    topic.delete()
    return redirect('core:history')

@login_required
def toggle_bookmark(request, topic_id):
    topic = get_object_or_404(TopicSearch, id=topic_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, topic=topic)
    if not created:
        bookmark.delete()
    return redirect(request.META.get('HTTP_REFERER', 'core:dashboard'))

@login_required
def profile_view(request):
    attempts = UserAttempt.objects.filter(user=request.user).order_by('-attempted_at')
    return render(request, 'core/profile.html', {'user': request.user, 'attempts': attempts})
