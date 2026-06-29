from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from projects.models import Project, Sprint
from tasks.models import Task
from users.models import User
import datetime

@login_required
def dashboard_view(request):
    user = request.user
    
    if user.is_admin:
        # Admin Dashboard data
        total_users = User.objects.count()
        active_projects = Project.objects.filter(status='ACTIVE').count()
        completed_projects = Project.objects.filter(status='COMPLETED').count()
        total_tasks = Task.objects.count()
        
        context = {
            'total_users': total_users,
            'active_projects': active_projects,
            'completed_projects': completed_projects,
            'total_tasks': total_tasks,
            'recent_projects': Project.objects.order_by('-created_at')[:5],
        }
        return render(request, 'core/admin_dashboard.html', context)
        
    elif user.is_manager:
        # Manager Dashboard data
        projects = Project.objects.filter(members__user=user)
        active_tasks = Task.objects.filter(project__in=projects).exclude(status='DONE').count()
        active_sprints = Sprint.objects.filter(project__in=projects, is_active=True).count()
        
        deadline_alerts = Task.objects.filter(
            project__in=projects, 
            status__in=['TODO', 'IN_PROGRESS', 'REVIEW'],
            due_date__lte=timezone.now().date() + datetime.timedelta(days=3)
        ).order_by('due_date')[:5]
        
        context = {
            'projects': projects[:5],
            'active_tasks': active_tasks,
            'active_sprints': active_sprints,
            'deadline_alerts': deadline_alerts,
        }
        return render(request, 'core/manager_dashboard.html', context)
        
    else:
        # Member Dashboard data
        assigned_tasks = Task.objects.filter(assignee=user).exclude(status='DONE')
        upcoming_deadlines = assigned_tasks.filter(
            due_date__lte=timezone.now().date() + datetime.timedelta(days=7)
        ).order_by('due_date')[:5]
        recent_activities = user.activity_logs.order_by('-timestamp')[:10]
        
        context = {
            'assigned_tasks': assigned_tasks[:5],
            'upcoming_deadlines': upcoming_deadlines,
            'recent_activities': recent_activities,
        }
        return render(request, 'core/member_dashboard.html', context)

@login_required
def global_search(request):
    q = request.GET.get('q', '')
    projects = []
    tasks = []
    users = []
    
    if q:
        projects = Project.objects.filter(Q(name__icontains=q) | Q(description__icontains=q))
        tasks = Task.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
        users = User.objects.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
        
        # Filter based on user role to avoid leaking data
        if not (request.user.is_admin or request.user.is_manager):
            projects = projects.filter(members__user=request.user)
            tasks = tasks.filter(project__members__user=request.user)
            
    context = {
        'q': q,
        'projects': projects,
        'tasks': tasks,
        'users': users
    }
    return render(request, 'core/global_search.html', context)

@login_required
def reports_view(request):
    from django.http import HttpResponseForbidden
    if not (request.user.is_admin or request.user.is_manager):
        return HttpResponseForbidden("You don't have permission to access reports.")
        
    projects = Project.objects.all() if request.user.is_admin else Project.objects.filter(members__user=request.user)
    
    total_tasks = Task.objects.filter(project__in=projects).count()
    completed_tasks = Task.objects.filter(project__in=projects, status='DONE').count()
    overdue_tasks = Task.objects.filter(project__in=projects, due_date__lt=timezone.now().date()).exclude(status='DONE').count()
    
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    context = {
        'projects': projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': completion_rate,
    }
    return render(request, 'core/reports.html', context)
