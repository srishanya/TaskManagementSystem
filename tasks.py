from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Task
from django.utils import timezone
import datetime

@shared_task
def send_task_assignment_email(task_id):
    try:
        task = Task.objects.get(pk=task_id)
        if task.assignee and task.assignee.email:
            subject = f"New Task Assigned: {task.title}"
            message = f"Hello {task.assignee.get_full_name() or task.assignee.username},\n\n" \
                      f"You have been assigned a new task: {task.title}\n" \
                      f"Project: {task.project.name}\n" \
                      f"Priority: {task.get_priority_display()}\n" \
                      f"Due Date: {task.due_date or 'No due date'}\n\n" \
                      f"Please check your dashboard for more details.\n"
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [task.assignee.email],
                fail_silently=False,
            )
            return f"Email sent to {task.assignee.email}"
        return "No assignee or email found"
    except Task.DoesNotExist:
        return f"Task {task_id} not found"

@shared_task
def check_approaching_deadlines():
    # Find tasks due in the next 2 days that are not completed
    target_date = timezone.now().date() + datetime.timedelta(days=2)
    tasks = Task.objects.filter(due_date=target_date).exclude(status='DONE')
    
    count = 0
    for task in tasks:
        if task.assignee and task.assignee.email:
            subject = f"Approaching Deadline: {task.title}"
            message = f"Hello {task.assignee.get_full_name() or task.assignee.username},\n\n" \
                      f"This is a reminder that the task '{task.title}' is due on {task.due_date}.\n" \
                      f"Please ensure it is completed on time.\n"
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [task.assignee.email],
                fail_silently=True,
            )
            count += 1
            
    return f"Sent {count} deadline reminder emails."
