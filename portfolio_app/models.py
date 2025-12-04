
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Custom manager for Student
class StudentManager(BaseUserManager):
    def create_user(self, username, password, full_name, email=None):
        if not username:
            raise ValueError("Username is required")
        user = self.model(username=username, full_name=full_name, email=email)
        user.set_password(password)  # Automatically hashes password
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, full_name, email=None):
        user = self.create_user(username=username, password=password, full_name=full_name, email=email)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Custom Student model
class Student(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = StudentManager()

    USERNAME_FIELD = 'username'  # Field used to login
    REQUIRED_FIELDS = ['full_name']  # Required when creating superuser

    def __str__(self):
        return self.username

class Project(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=200)
    description = models.TextField()

class Skill(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)  # halimbawa: Beginner, Intermediate, Advanced
