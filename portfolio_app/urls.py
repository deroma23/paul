from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.add_student, name='add_student'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_project/', views.add_project, name='add_project'),
    path('add_skill/', views.add_skill, name='add_skill'),
    path('portfolio/<int:student_id>/', views.portfolio, name='portfolio'),
    path('api/portfolio/<int:student_id>/', views.portfolio_api, name='portfolio_api'),
]
