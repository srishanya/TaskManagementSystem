from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, ProjectMember, Sprint
from .forms import ProjectForm, ProjectMemberForm, SprintForm

from django.db.models import Q

@login_required
def project_list(request):
    if request.user.is_admin or request.user.is_manager:
        projects = Project.objects.all().order_by('-created_at')
    else:
        projects = Project.objects.filter(members__user=request.user).order_by('-created_at')
        
    q = request.GET.get('q')
    if q:
        projects = projects.filter(Q(name__icontains=q) | Q(description__icontains=q))
        
    return render(request, 'projects/project_list.html', {'projects': projects})

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    
    # Check access
    if not (request.user.is_admin or request.user.is_manager or project.members.filter(user=request.user).exists()):
        messages.error(request, "You don't have access to this project.")
        return redirect('projects:project_list')

    members = project.members.select_related('user').all()
    tasks = project.tasks.all() # We will use this later

    # Calculate dashboard metrics
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='DONE').count()
    pending_tasks = total_tasks - completed_tasks
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return render(request, 'projects/project_detail.html', {
        'project': project,
        'members': members,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'completion_percentage': completion_percentage
    })

@login_required
def project_create(request):
    if not (request.user.is_admin or request.user.is_manager):
        messages.error(request, "Only Administrators and Project Managers can create projects.")
        return redirect('projects:project_list')

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            # Add creator as ADMIN member
            ProjectMember.objects.create(project=project, user=request.user, role='ADMIN')
            messages.success(request, 'Project created successfully!')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = ProjectForm()
    
    return render(request, 'projects/project_form.html', {'form': form, 'action': 'Create'})

@login_required
def project_add_member(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not (request.user.is_admin or request.user.is_manager):
        messages.error(request, "You don't have permission to add members.")
        return redirect('projects:project_detail', pk=project.pk)

    if request.method == 'POST':
        form = ProjectMemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.project = project
            try:
                member.save()
                messages.success(request, 'Member added successfully!')
                return redirect('projects:project_detail', pk=project.pk)
            except Exception as e:
                messages.error(request, 'This user is already a member of the project.')
    else:
        form = ProjectMemberForm()
    
    
    return render(request, 'projects/project_member_form.html', {'form': form, 'project': project})

@login_required
def sprint_create(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not (request.user.is_admin or request.user.is_manager):
        messages.error(request, "Only Administrators and Project Managers can create sprints.")
        return redirect('projects:project_detail', pk=project.pk)

    if request.method == 'POST':
        form = SprintForm(request.POST)
        if form.is_valid():
            sprint = form.save(commit=False)
            sprint.project = project
            sprint.save()
            messages.success(request, 'Sprint created successfully!')
            return redirect('projects:project_detail', pk=project.pk)
    else:
        form = SprintForm()
    
    return render(request, 'projects/sprint_form.html', {'form': form, 'project': project})

@login_required
def sprint_detail(request, pk):
    sprint = get_object_or_404(Sprint, pk=pk)
    project = sprint.project
    
    if not (request.user.is_admin or request.user.is_manager or project.members.filter(user=request.user).exists()):
        messages.error(request, "You don't have access to this sprint.")
        return redirect('projects:project_list')

    tasks = sprint.tasks.all()
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='DONE').count()
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0

    return render(request, 'projects/sprint_detail.html', {
        'sprint': sprint,
        'project': project,
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_percentage': completion_percentage
    })
