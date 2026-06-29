# Task Scheduling and Project Management System (Jira/Taiga-like)
## Goal Description
Build a comprehensive Task Scheduling and Project Management System using Django, Django REST Framework, PostgreSQL, and Celery/Redis for background tasks. The application will allow teams to manage projects, schedule tasks, track progress via Kanban and Sprints, collaborate (comments, file uploads), and view dashboards and reports.

## User Review Required
IMPORTANT

This system is massive and involves multiple interconnected modules (Auth, Projects, Tasks, Kanban, Sprints, Comments, Files, Notifications, Scheduling). I propose an iterative approach to development to ensure high quality and correct behavior. The plan below outlines the full scope, but we will execute it in phases, starting with the foundational features (Auth, Projects, Tasks). Please review the architecture, technology choices, and the proposed phases.

## Open Questions
Frontend Architecture: The requirements list standard HTML/Bootstrap with React as optional. Should we build this entirely using Django Templates (Server-Side Rendered) with vanilla JS for interactivity (like drag-and-drop), or do you want an API-first application with a decoupled React frontend? I will proceed with Django Templates + Bootstrap + DRF APIs for background tasks by default.
Authentication Flow: The prompt mentions JWT Auth. If we use Django Templates, session authentication is standard and more secure for the web UI. We can expose JWT for the DRF APIs (for mobile apps or future SPA). Does this mixed approach sound good?

## Environment:
Do you have PostgreSQL and Redis installed locally on your Windows machine, or should we use Docker/Docker Compose to easily spin up the database and Redis instances?

## Proposed Architecture and Phases
We will break the development into 5 manageable phases:

Phase 1: Core Foundation and Authentication (Modules 1 & 2)
Setup: Django project creation, configure PostgreSQL, setup Celery/Redis.
Models: Custom User model, Role Management (Admin, PM, Team Member).
Features: Registration, Login, Password Reset, Profile Management.
Phase 2: Project & Basic Task Management (Modules 3 & 4)
Models: Project, ProjectMember, Task.
Features: Create projects, assign team members, create tasks, prioritize, assign, and update task status.
Phase 3: Agile workflows & Visualization (Modules 5, 6, & 7)
Models: Sprint, TaskDependency.
Features: Sprint creation/tracking, Kanban Board view (with drag-and-drop), Calendar/Gantt chart foundations.
Phase 4: Collaboration & File Management (Modules 8 & 9)
Models: Comment, Attachment, ActivityLog.
Features: Task comments, @mentions, file uploads for tasks/projects, and activity tracking.
Phase 5: Notifications, Reporting & Dashboards (Modules 10, 11, 12, & 13)
Models: Notification.
Features: Celery-powered email and in-app notifications, advanced search/filtering, Role-specific dashboards (Admin, PM, Member).
Proposed Changes
We will create a monolithic Django application with logical module separation:

## Project Level
[NEW] requirements.txt
[NEW] docker-compose.yml (Recommended for Postgres/Redis setup)
[NEW] task_manager/settings.py (Core Django settings, DB, Celery, DRF configs)
Django Apps
[NEW] apps/users/ (Auth, Profiles, Roles)
[NEW] apps/projects/ (Projects, Sprints, Team Assignments)
[NEW] apps/tasks/ (Tasks, Kanban, Comments, Attachments, Activity Logs)
[NEW] apps/notifications/ (In-App Notifications, Email handling via Celery)
[NEW] apps/core/ (Dashboards, Search, Reports, Shared UI templates)

## Verification Plan
Automated Tests
We will write Django tests (TestCase) and pytest for core business logic, especially around Role-Based Access Control (e.g., verifying a Team Member cannot delete a Project).

## Manual Verification
Since this is a highly interactive application (Kanban boards, calendar views, real-time-like notifications), we will heavily rely on manual testing of the UI flows locally. We'll verify that Celery workers process background jobs successfully.
