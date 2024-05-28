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
    calendar=models.OneToOneField('Calendars',on_delete=models.SET_NULL,related_name='teacher_calendar',null=True, blank=True)    
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


class TimeSlot(models.Model):
    DAY_CHOICES = [
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),

    ]
    TIME_RANGES = [
    ('7:00 - 8:00', '7:00 - 8:00'),
    ('8:00 - 9:00', '8:00 - 9:00'),
    ('9:00 - 10:00', '9:00 - 10:00'),
    ('10:00 - 11:00', '10:00 - 11:00'),
    ('11:00 - 12:00', '11:00 - 12:00'),
    ('12:00 - 1:00', '12:00 - 1:00'),
    ('1:00 - 2:00', '1:00 - 2:00'),
    ('2:00 - 3:00', '2:00 - 3:00'),
    ('3:00 - 4:00', '3:00 - 4:00'),
    ('4:00 - 5:00', '4:00 - 5:00'),
    ('5:00 - 6:00', '5:00 - 6:00'),


     ]

    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    time_range= models.CharField(max_length=13, choices=TIME_RANGES, default='8:00 - 9:00', null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    subject= models.ForeignKey(Subject, on_delete=models.SET_NULL, related_name='timeslots', null=True, blank=True)
    calendar = models.ForeignKey('Calendars', on_delete=models.CASCADE, related_name='timeslots', null= True)

    def __str__(self):
        return f'{self.get_day_display()}  {self.time_range}'

class Calendars(models.Model):
    title = models.CharField(max_length=255)
    CALENDAR_TYPES = [
        ('CLASS', 'Classroom Schedule'),
        ('CAFE', 'Cafeteria Menu'),
        ('EVENT', 'Events'),
    ]
    calendar_type = models.CharField(max_length=5, choices=CALENDAR_TYPES, default='CLASS')
    start_week = models.DateField(null=True, blank=True)
    end_week = models.DateField(null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Calendars'

    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.timeslots.exists():
            if self.calendar_type == 'CLASS':
                days = TimeSlot.DAY_CHOICES[1:6]  # Sunday to Thursday
                time_ranges = TimeSlot.TIME_RANGES[1:4] + TimeSlot.TIME_RANGES[6:9]            
            elif self.calendar_type == 'CAFE':
                days = TimeSlot.DAY_CHOICES[1:6]  # Sunday to Thursday
                time_ranges = [('12:00 - 1:00', '12:00 - 1:00')]  # 12:00 to 1:00
            else:  # 'EVENT'
                days = TimeSlot.DAY_CHOICES  # All days
                time_ranges = TimeSlot.TIME_RANGES  # All time ranges

            for day in days:
                for time_range in time_ranges:
                    TimeSlot.objects.create(day=day[0], time_range=time_range[0], calendar=self)
    

    
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
    
    teachers=models.ManyToManyField(Teacher, related_name='classrooms', blank=True)

    school_year=models.CharField(max_length=9,null=True)
    subjects = models.ManyToManyField(Subject, related_name='classrooms', blank=True)
    calendar = models.ForeignKey(Calendars, on_delete=models.CASCADE, related_name='calendar', null=True)


    def __str__(self):
        return self.name
    


def limit_to_students():
    return {'user_type': 'student'}

class Grade(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='grades')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_grades',null=True)
    trimester= models.IntegerField(null=True)
    grade = models.IntegerField(null=True)
    GRADE_TYPE_CHOICES = [('Continous','Continous'),('Test','Test'),('Exam','Exam')]
    GRADE_TYPE_WEIGHTS = {'Continous': 1/4, 'Test': 1/4, 'Exam': 2/4}
    grade_type = models.CharField(max_length=30, choices=GRADE_TYPE_CHOICES, default='Continous')

    @property
    def weight(self):
        return self.GRADE_TYPE_WEIGHTS[self.grade_type]

    def get_trimester_ordinal(self):
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(self.trimester % 10, 'th')
        return str(self.trimester) + suffix

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.grade} "
    
    #overriding save method to prevent duplicate grades
    def save(self, *args, **kwargs):
        try:
            existing= Grade.objects.get(subject=self.subject, student=self.student, grade_type =self.grade_type, trimester=self.trimester)
            if existing.pk != self.pk:
                self.pk = existing.pk
        except Grade.DoesNotExist:
            pass
        super().save(*args, **kwargs)

class Absences(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='absences')
    TRIMESTER_CHOICES =[('1','1'),('2','2'),('3','3')]
    trimester = models.CharField(max_length=1, choices=TRIMESTER_CHOICES, default='1')
    school_year=models.CharField(max_length=9,null=True)
    date = models.DateField()
    is_justified=models.BooleanField(default=False)
    JUSTIFICATION_CHOICES = [('Parent','Parent'),('Medical','Medical'),('Other','Other')]
    justification=models.CharField(max_length=30, choices=JUSTIFICATION_CHOICES, default='Parent', blank='True')
    
    def __str__(self):
        return f"{self.student.user.first_name}{self.student.user.last_name}  - {self.date}"
    


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
    
class HomeworkAssignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='homeworks')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='homeworks')
    assignment_file= models.FileField(upload_to='homeworks_assignments/', null=True, blank=True)
    classroom= models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='homeworks', null=True)

    class Meta:
        verbose_name = 'Homework'
    def __str__(self):
        return self.title

class HomeworkSubmission(models.Model):
    homework = models.ForeignKey(HomeworkAssignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='homework_submissions')
    response=models.CharField(max_length=255, null=True, blank=True)
    submission_file = models.FileField(upload_to='homework_submissions/', null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.user.first_name}{self.student.user.last_name} - {self.homework.title}"
    class Meta:
        unique_together =('homework','student')



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
