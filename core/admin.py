from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.urls import path
from .models import Contact, CustomUser, Classroom,Grade, HomeworkSubmission, Subject, Calendars, Absences, Announcements,Remarks,HomeworkAssignment,Courses, Teacher, Student, Parent, TimeSlot



class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Subject, SubjectAdmin)

# class GradeInline(admin.TabularInline):
#     model = Grade
#     extra = 0
#     verbose_name_plural = 'Grades'
#     pk_filed='student'  



class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'teacher information'  

class ParentInline(admin.TabularInline):
    model = Parent
    extra = 0
    verbose_name_plural = 'Parent information' 



class StudentInline(admin.TabularInline):
    model = Student
    extra = 0
    verbose_name_plural = 'Student information' 
    

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [TeacherInline, StudentInline] 
    search_fields = ['username','first_name','last_name','email']
    list_filter = ('groups',)

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj is not None and obj.user_type == 'parent':
             inline_instance = ParentInline(self.model, self.admin_site)
             inline_instances.append(inline_instance)
        elif obj is not None and obj.user_type == 'student':

            inline_instance = StudentInline(self.model, self.admin_site)
            inline_instances.append(inline_instance)

        elif obj is not None and obj.user_type == 'teacher':
            inline_instance = TeacherInline(self.model, self.admin_site)
            inline_instances.append(inline_instance)
        
        return inline_instances
 
    def get_exclude(self, request, obj=None):
        exclude = super().get_exclude(request, obj) or []
        if obj and obj.user_type != 'student':
            exclude = list(exclude)  # Convert to list to append, get exclude returned a tuple
            exclude.append('matricule')
        return exclude  #don't need this remove later
    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj and obj.user_type == 'parent':
            return readonly_fields + ('childrens_info',)
        return readonly_fields
    def childrens_info(self, obj):
        if obj.user_type == 'parent':
            parent = Parent.objects.get(user=obj)
            students = parent.children.all()
            return ', '.join(str(student) for student in students)
        return "Not a parent"

    childrens_info.short_description = 'Children'  # Optional: Set a custom label for the field in the admin

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user_type='parent')
  

admin.site.register(CustomUser, CustomUserAdmin)

class StudentsInline(admin.TabularInline):
    model = Student
    extra = 0
    verbose_name_plural = 'Students'
    can_delete = False
    max_num = 0

    def has_change_permission(self, request, obj=None):
        return False   


class ClassroomAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [StudentsInline]
    list_filter = ['level','school_year']
    filter_horizontal = ['subjects']
    change_form_template = 'admin/core/classroom/change_form.html'
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:pk>/change/assign-grades/', self.admin_site.admin_view(self.assign_grades), name='assign-grades'),
        ]
        return custom_urls + urls

    def assign_grades(self, request, pk):
        classroom = get_object_or_404(Classroom, pk=pk)
        return render(request, 'core/grades/assign_grades.html')

admin.site.register(Classroom, ClassroomAdmin)


admin.site.site_header = "El-Hikma school Admin"
admin.site.site_title = " El-Hikma school Admin Portal"
admin.site.index_title = "Welcome to El-Hikma school Admin"



class AbsencesAdmin(admin.ModelAdmin):
    model: Absences
    search_fields=['student__user__username','student__user__last_name','student__user__first_name']


admin.site.register(Absences, AbsencesAdmin)

class AnnouncementsAdmin(admin.ModelAdmin):
    model:Announcements
    search_fields=['title','category']


admin.site.register(Announcements, AnnouncementsAdmin)

class RemarksAdmin(admin.ModelAdmin):
    model:Remarks
    search_fields=['student__user__username','student__user__last_name','student__user__first_name']

admin.site.register(Remarks, RemarksAdmin)

class CoursesAdmin(admin.ModelAdmin):
    model:Courses
    search_fields=['title', 'level', 'subject']
admin.site.register(Courses, CoursesAdmin)


class HomeworkSubmissionInline(admin.TabularInline):
    model =HomeworkSubmission
    extra=0
    verbose_name_plural = 'Homework Submissions'
    
class HomeworkAssignmentAdmin(admin.ModelAdmin):
    inlines = [HomeworkSubmissionInline]
    search_fields = ['title', 'subject__name']


admin.site.register(HomeworkAssignment, HomeworkAssignmentAdmin)

class GradeAdmin(admin.ModelAdmin):
     search_fields=['student__user__username','student__user__last_name','student__user__first_name']
     list_filter= ['subject']


admin.site.register(Grade, GradeAdmin)



class TimeSlotsInline(admin.TabularInline):
    model = TimeSlot
    extra = 0
    verbose_name_plural = 'TimeSlots'
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)

        # If the parent Calendar object exists and its calendar_type is 'CLASS',
        # only display the 'day', 'time_range', and 'subject' fields in the formset.
        # Otherwise, display the 'day', 'time_range', and 'content' fields.
        if obj and obj.calendar_type == 'CLASS':
            formset.form.base_fields = {k: v for k, v in formset.form.base_fields.items() if k in ['day', 'time_range', 'subject']}
        else:
            formset.form.base_fields = {k: v for k, v in formset.form.base_fields.items() if k in ['day', 'time_range', 'content']}

        return formset

class CalendarAdmin(admin.ModelAdmin):
    inlines = [TimeSlotsInline]
    exclude = ('timeslots',)
    search_fields = ['title']
    verbose_name_plural = 'Calendars'

# admin.site.register(TimeSlot)

admin.site.register(Calendars, CalendarAdmin)

# admin.py

# admin.py

from django.contrib import admin
from .models import Student, Grade, Subject

def create_grades(modeladmin, request, queryset):
    for student in queryset:
        if student.classroom:
            subjects = student.classroom.subjects.all()
            for subject in subjects:
                for trimester in range(1, 4):  # Including all 3 trimesters
                    for grade_type in ['Continous', 'Test', 'Exam']:
                        Grade.objects.get_or_create(
                            student=student,
                            subject=subject,
                            trimester=trimester,
                            grade_type=grade_type,
                            defaults={'grade': 0}
                        )
        else:
            modeladmin.message_user(request, f"Student {student} does not belong to any classroom.", level='error')
    modeladmin.message_user(request, "Grades have been created successfully.")

create_grades.short_description = "Create empty grades for selected students"

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'classroom', 'parent', 'matricule', 'gender')
    actions = [create_grades]





class GradeInline(admin.TabularInline):
    model = Grade
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'classroom', 'parent', 'matricule', 'age')
    inlines = [GradeInline]
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    actions = [create_grades]



    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'  # Sets column header

    def age(self, obj):
        return obj.age
    age.short_description = 'Age'

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ('user', 'user_username')
        return readonly_fields

admin.site.register(Student, StudentAdmin)


class ParentAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'childrens_info')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']


    def user_username(self, obj):
        return obj.user.username
    user_username.short_description = 'Username'  # Sets column header

    def childrens_info(self, obj):
        students = obj.children.all()
        return ', '.join(str(student) for student in students)
    childrens_info.short_description = 'Children'  # Sets column header

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ('user', 'user_username', 'childrens_info')
        return readonly_fields

admin.site.register(Parent, ParentAdmin)

class SubjectInline(admin.TabularInline):
    model = Subject.teachers.through
    extra = 1

class ClassroomInline(admin.TabularInline):
    model = Classroom.teachers.through
    extra = 1

class TeacherAdmin(admin.ModelAdmin):
    inlines = (SubjectInline, ClassroomInline)
    exclude = ('subjects', 'classrooms')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super().get_readonly_fields(request, obj)
        if obj:
            return readonly_fields + ('user',)
        return readonly_fields

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Contact)