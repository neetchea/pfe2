from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.hashers import make_password



class CustomUser(AbstractUser):
    
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
        ('admin/staff', 'Admin/Staff')
    )

    user_type = models.CharField(max_length=30, choices=USER_TYPE_CHOICES)

    def save(self, *args, **kwargs):
        #so i don't double hash password and i do hash password on password change
        # Check if the user already exists
        if self.pk:
            orig = CustomUser.objects.get(pk=self.pk)
            if orig.password != self.password:  # The password has been changed
                self.password = make_password(self.password)
        else:  # This is a new user
            self.password = make_password(self.password)
            super().save(*args, **kwargs)  # Save the user first, because the user needs to exist before creating the related instance

            # Create the associated Teacher, Student, or Parent instance if it doesn't already exist
            if self.user_type == 'teacher' and not hasattr(self, 'teacher'):
                Teacher.objects.create(user=self)
            elif self.user_type == 'student' and not hasattr(self, 'student'):
                Student.objects.create(user=self)
            elif self.user_type == 'parent' and not hasattr(self, 'parent'):
                Parent.objects.create(user=self)
            return

        super().save(*args, **kwargs)

class Teacher(models.Model):
    user= models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='teacher')
    calendar=models.OneToOneField('Calendars',on_delete=models.SET_NULL,related_name='teacher_calendar',null=True)    
    class Meta:
        verbose_name = 'Teacher information'
        verbose_name_plural = 'Teachers information'
    def __str__(self):
        return self.user.username
         
class Student(models.Model):
    user= models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='student')
    classroom= models.ForeignKey('Classroom',on_delete=models.SET_NULL,related_name='student',null=True, blank=True)
    parent=models.ForeignKey('Parent',on_delete=models.SET_NULL,related_name='children',null=True,blank=True)
    matricule=models.CharField(max_length=30,null=True,blank=True)
    class Meta:
        verbose_name = 'Student information'
        verbose_name_plural = 'Students information'
    def __str__(self):
        return self.user.username

class Parent(models.Model):
    user= models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='parent')
    class Meta:
        verbose_name = 'Parent information'
        verbose_name_plural = 'Parents information'
    def __str__(self):
        return self.user.username
        
class Subject(models.Model):
    name = models.CharField(max_length=255)
    coefficient = models.IntegerField()
    teachers=models.ManyToManyField(Teacher, related_name='subjects')

    # classroom= models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='subjects', null=True)
    # def save(self, *args, **kwargs):
    #     if self.classroom:
    #         self.level = self.classroom.level  # Ensure level matches the classroom

    #     old_teacher = None
    #     if self.pk:
    #         old_teacher = Subject.objects.get(pk=self.pk).teacher

    #     super().save(*args, **kwargs)  # Call the "real" save() method.

    #     if self.classroom:
    #         # Add new teacher to the classroom
    #         if self.teacher and self.teacher not in self.classroom.teachers.all():
    #             self.classroom.teachers.add(self.teacher)

    #         # Remove teacher who is no longer teaching any subjects in the classroom
    #         if old_teacher and old_teacher != self.teacher:
    #             other_subjects = self.classroom.subjects.exclude(id=self.id)
    #             if not other_subjects.filter(teacher=old_teacher).exists():
    #                 self.classroom.teachers.remove(old_teacher)
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
    
    teachers=models.ManyToManyField(Teacher, related_name='classrooms', null=True, blank=True)

    school_year=models.CharField(max_length=9,null=True)
    subjects = models.ManyToManyField(Subject, related_name='classrooms', blank=True)

    def __str__(self):
        return self.name
    


def limit_to_students():
    return {'user_type': 'student'}

class Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='student_grades',null=True, limit_choices_to={'user_type': 'student'})
    trimester= models.IntegerField(null=True)
    grade = models.IntegerField(null=True)
    GRADE_TYPE_CHOICES = [('Continous','Continous'),('Test','Test'),('Exam','Exam'),('Final','Final')]
    grade_type = models.CharField(max_length=30, choices=GRADE_TYPE_CHOICES, default='Continous')
    def get_trimester_ordinal(self):
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(self.trimester % 10, 'th')
        return str(self.trimester) + suffix

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade} "

class Absences(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='absences')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='absences')
    date = models.DateField()
    justification = models.TextField(blank=True)
    number_of_absences=models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.date}"
    
class Calendars(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    all_day = models.BooleanField(default=False)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='calendars', null=True)
    
    def __str__(self):
        return self.title
    

class Courses(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    all_day = models.BooleanField(default=False)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    def __str__(self):
        return self.title
    
class Homework(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='homeworks')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='homeworks')
    student= models.OneToOneField(Student, related_name='homeworks',on_delete=models.SET_NULL,null=True, blank=True) 
    def __str__(self):
        return self.title

class Remarks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='remarks')
    trimester= models.IntegerField(null=True)
    date = models.DateField()
    remark = models.TextField()
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='remarks_written')
    def __str__(self):
        return f"{self.student} - {self.teacher} - {self.date}"
    
class Announcements(models.Model):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Academic', 'Academic'),
        ('Recruitment', 'Recruitment'),
        ('Events', 'Events'),
        ('Trips', 'Trips'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    category=models.CharField(max_length=255, choices=CATEGORY_CHOICES, default='General')
    is_user_only= models.BooleanField(default=False)
    active=models.BooleanField(default=False)
    photo= models.ImageField(upload_to='announcements/', null=True, blank=True)
    def __str__(self):
        return self.title
