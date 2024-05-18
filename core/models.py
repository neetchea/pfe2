from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password
def limit_to_students():
    return {'user_type': 'Student'}
class CustomUser(AbstractUser):
    
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES,blank=True, null=True)
    matricule=models.CharField(max_length=255, blank=True,null=True, unique=True)


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

class Subject(models.Model):
    name = models.CharField(max_length=255)
    coefficient = models.IntegerField()
    teacher= models.ForeignKey(CustomUser,related_name='subjects',on_delete=models.SET_NULL, limit_choices_to={'user_type': 'teacher'}, null=True)
    # classroom= models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='subjects', null=True)
    def save(self, *args, **kwargs):
        if self.classroom:
            self.level = self.classroom.level  # Ensure level matches the classroom

        old_teacher = None
        if self.pk:
            old_teacher = Subject.objects.get(pk=self.pk).teacher

        super().save(*args, **kwargs)  # Call the "real" save() method.

        if self.classroom:
            # Add new teacher to the classroom
            if self.teacher and self.teacher not in self.classroom.teachers.all():
                self.classroom.teachers.add(self.teacher)

            # Remove teacher who is no longer teaching any subjects in the classroom
            if old_teacher and old_teacher != self.teacher:
                other_subjects = self.classroom.subjects.exclude(id=self.id)
                if not other_subjects.filter(teacher=old_teacher).exists():
                    self.classroom.teachers.remove(old_teacher)
    def __str__(self):
        return self.name

class Classroom(models.Model):
    name = models.CharField(max_length=255)

    LEVEL_CHOICES = [
        ('P1', 'Preparatory 1'),
        ('P2', 'Preparatory 2'),
        ('E1', 'Elementary 1'),
        ('E2', 'Elementary 2'),
        ('E3', 'Elementary 3'),
        ('E4', 'Elementary 4'),
        ('E5', 'Elementary 5'),
        ('M1', 'Middle 1'),
        ('M2', 'Middle 2'),
        ('M3', 'Middle 3'),
        ('M4', 'Middle 4'),
    ]

    
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    
    teachers = models.ManyToManyField(
        CustomUser,
        limit_choices_to={'user_type': 'teacher'},
        related_name='classes_enseignées', blank=True
    )
    school_year=models.CharField(max_length=9,null=True)
    subjects = models.ManyToManyField(Subject, related_name='classrooms', blank=True)

    def __str__(self):
        return self.name
    

class StudentInClassroom(models.Model):
    student = models.ManyToManyField(
        CustomUser,
        related_name='classroom_assignment',
        limit_choices_to={'user_type': 'student'},
        
    )
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)


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



class Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='grades', limit_choices_to={'user_type': 'student'})
    trimester= models.IntegerField(null=True)
    grade = models.IntegerField(null=True)

    def get_trimester_ordinal(self):
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(self.trimester % 10, 'th')
        return str(self.trimester) + suffix

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade} - {self.subject.teacher}"