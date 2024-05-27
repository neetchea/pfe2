from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.urls import path
from .models import CustomUser, Classroom,Grade, HomeworkSubmission, Subject, Calendars, Absences, Announcements,Remarks,HomeworkAssignment,Courses, Teacher, Student, Parent



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
    search_fields = ['username']
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
admin.site.register(Grade)


admin.site.site_header = "El-Hikma school Admin"
admin.site.site_title = " El-Hikma school Admin Portal"
admin.site.index_title = "Welcome to El-Hikma school Admin"
admin.site.register(Calendars)
admin.site.register(Absences)
admin.site.register(Announcements)
admin.site.register(Remarks)
admin.register(Courses)


class HomeworkSubmissionInline(admin.TabularInline):
    model =HomeworkSubmission
    extra=0
    verbose_name_plural = 'Homework Submissions'
    
class HomeworkAssignmentAdmin(admin.ModelAdmin):
    inlines = [HomeworkSubmissionInline]
    search_fields = ['title', 'subject__name']


admin.site.register(HomeworkAssignment, HomeworkAssignmentAdmin)