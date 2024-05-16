from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password

class CustomUser(AbstractUser):
    
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    matricule=models.CharField(max_length=255, blank=True,
                               null=True, unique=True)

    def save(self, *args, **kwargs):
        #so i don't double hash password and i do hash password on password change
        # Check if the user already exists
        if self.pk:
            orig = CustomUser.objects.get(pk=self.pk)
            if orig.password != self.password:  # The password has been changed
                self.password = make_password(self.password)
        else:  # This is a new user
            self.password = make_password(self.password)
        super().save(*args, **kwargs)


class Classroom(models.Model):
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=255)
    teacher = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'teacher'},
        related_name='classes_enseignées'
    )
    students = models.ManyToManyField(
        CustomUser,
        limit_choices_to={'user_type': 'student'},
        related_name='classe'
    )

    class Meta:
        verbose_name = "Classe"
        verbose_name_plural = "Classes"

    def __str__(self):
        return self.name


class ParentChildRelationship(models.Model):
    parent = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='children',
        limit_choices_to={'user_type': 'parent'}
    )
    child = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='parents',
        limit_choices_to={'user_type': 'student'}
    )

class Subject(models.Model):
    name = models.CharField(max_length=255)
    coefficient = models.IntegerField()
    teacher= models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='subjects', limit_choices_to={'user_type: teacher'})

    def __str__(self):
        return self.name

class Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='grades', limit_choices_to={'user_type': 'student'})
    note_module = models.IntegerField()

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.note_module}"