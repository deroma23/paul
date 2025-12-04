from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Project, Skill
from .forms import StudentRegistrationForm, ProjectForm, SkillForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# View para mag-register ng student
def add_student(request):
    """
    Ang view na ito ay nagre-render ng form para sa pag-register ng student
    at nagse-save ng student sa database gamit ang ORM methods.
    """
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()  # ORM: mag-save sa Student table
            login(request, student)  # automatic login after registration
            return redirect('dashboard')  # after login redirect sa dashboard
    else:
        form = StudentRegistrationForm()
    return render(request, 'add_student.html', {'form': form})

# Dashboard para mag-add ng projects at skills
@login_required
def dashboard(request):
    student = request.user
    projects = student.projects.all()
    skills = student.skills.all()
    return render(request, 'dashboard.html', {'student': student, 'projects': projects, 'skills': skills})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = request.user
            project.save()
            return redirect('dashboard')
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})

@login_required
def add_skill(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.student = request.user
            skill.save()
            return redirect('dashboard')
    else:
        form = SkillForm()
    return render(request, 'add_skill.html', {'form': form})

# Public portfolio page
def portfolio(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    projects = student.projects.all()
    skills = student.skills.all()
    return render(request, 'portfolio.html', {'student': student, 'projects': projects, 'skills': skills})

# API endpoint para sa portfolio (JSON)
def portfolio_api(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    projects = list(student.projects.values())
    skills = list(student.skills.values())
    data = {
        'student': {'id': student.id, 'username': student.username, 'full_name': student.full_name},
        'projects': projects,
        'skills': skills
    }
    return JsonResponse(data)
