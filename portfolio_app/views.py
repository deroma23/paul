from django.shortcuts import render, redirect, get_object_or_404
from .models import Student, Project, Skill
from .forms import StudentRegistrationForm, ProjectForm, SkillForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# ------------------------------
# View para mag-register ng student
# ------------------------------
def add_student(request):
    """
    Ang view na ito ay nagre-render ng form para sa pag-register ng student
    at nagse-save ng student sa database gamit ang ORM methods.
    - Kung POST request, kino-validate ang form at ise-save ang student sa DB.
    - Automatic na nag-login ang student pagkatapos mag-register.
    - Redirect sa 'dashboard' pagkatapos ng successful registration.
    - Kung GET request, ire-render ang empty registration form.
    """
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()  # ORM: mag-save sa Student table
            login(request, student)  # automatic login after registration
            return redirect('dashboard')  # redirect sa dashboard page
    else:
        form = StudentRegistrationForm()
    return render(request, 'add_student.html', {'form': form})  # render form sa template

# ------------------------------
# Dashboard para mag-add ng projects at skills
# ------------------------------
@login_required
def dashboard(request):
    """
    View para sa dashboard ng logged-in student.
    - Kinukuha ang kasalukuyang logged-in user gamit request.user.
    - Kinukuha ang lahat ng projects at skills ng student.
    - Ire-render ang 'dashboard.html' template na may student, projects, at skills.
    """
    student = request.user
    projects = student.projects.all()  # lahat ng projects ng student
    skills = student.skills.all()      # lahat ng skills ng student
    return render(request, 'dashboard.html', {'student': student, 'projects': projects, 'skills': skills})

# ------------------------------
# View para mag-add ng project
# ------------------------------
@login_required
def add_project(request):
    """
    View para mag-add ng project ng student.
    - Kung POST request, kino-validate ang form.
    - Hindi muna directly sine-save (commit=False) para maidagdag ang student field.
    - Ise-save ang project sa database at ireredirect sa dashboard.
    - Kung GET request, ire-render ang empty ProjectForm.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)  # create project instance pero hindi pa save
            project.student = request.user     # assign ang logged-in student
            project.save()                     # i-save sa DB
            return redirect('dashboard')       # redirect sa dashboard
    else:
        form = ProjectForm()
    return render(request, 'add_project.html', {'form': form})  # render form sa template

# ------------------------------
# View para mag-add ng skill
# ------------------------------
@login_required
def add_skill(request):
    """
    View para mag-add ng skill ng student.
    - Katulad ng add_project, kino-validate ang form.
    - Assign sa logged-in student bago i-save.
    - Redirect sa dashboard pagkatapos ng successful save.
    """
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)   # create skill instance pero hindi pa save
            skill.student = request.user      # assign ang logged-in student
            skill.save()                      # i-save sa DB
            return redirect('dashboard')      # redirect sa dashboard
    else:
        form = SkillForm()
    return render(request, 'add_skill.html', {'form': form})  # render form sa template

# ------------------------------
# Public portfolio page
# ------------------------------
def portfolio(request, student_id):
    """
    Public view para makita ang full portfolio ng isang student.
    - Kukunin ang student object gamit ang get_object_or_404.
    - Kukuhanin lahat ng projects at skills ng student.
    - Ire-render sa 'portfolio.html' template.
    """
    student = get_object_or_404(Student, id=student_id)
    projects = student.projects.all()
    skills = student.skills.all()
    return render(request, 'portfolio.html', {'student': student, 'projects': projects, 'skills': skills})

# ------------------------------
# API endpoint para sa portfolio (JSON)
# ------------------------------
def portfolio_api(request, student_id):
    """
    API endpoint na nagre-return ng portfolio sa JSON format.
    - Kukunin ang student gamit ang ID.
    - Projects at skills ay icoconvert sa list of dictionaries gamit values().
    - Ire-return bilang JSON response.
    """
    student = get_object_or_404(Student, id=student_id)
    projects = list(student.projects.values())
    skills = list(student.skills.values())
    data = {
        'student': {'id': student.id, 'username': student.username, 'full_name': student.full_name},
        'projects': projects,
        'skills': skills
    }
    return JsonResponse(data)  # return JSON response
