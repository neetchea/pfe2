from django.contrib import admin
from django.shortcuts import get_object_or_404, render
from django.urls import path
from .models import CustomUser, Classroom, ParentChildRelationship,StudentInClassroom, Grade, Subject, Calendars, Absences, Announcements,Remarks,Homework,Courses
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ['name']

admin.site.register(Subject, SubjectAdmin)

class ParentChildInline(admin.TabularInline):
    model = ParentChildRelationship
    fk_name = 'parent'
    extra = 0 

class GradeInline(admin.TabularInline):
    model = Grade
    extra = 0  
    autocomplete_fields = ['subject']  
    fk_name = 'student'
    
    

class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ParentChildInline,GradeInline]
    search_fields = ['username']
    list_filter = ('groups',)

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj is not None and obj.user_type == 'parent':
             inline_instance = ParentChildInline(self.model, self.admin_site)
             inline_instances.append(inline_instance)
        elif obj is not None and obj.user_type == 'student':
            inline_instance = GradeInline(self.model, self.admin_site)
            inline_instances.append(inline_instance)
        return inline_instances
 
    def get_exclude(self, request, obj=None):
        exclude = super().get_exclude(request, obj) or []
        if obj and obj.user_type != 'student':
            exclude = list(exclude)  # Convert to list to append, get exclude returned a tuple
            exclude.append('matricule')
        return exclude


admin.site.register(CustomUser, CustomUserAdmin)

class StudentInClassroomInline(admin.TabularInline):
    model = StudentInClassroom
    extra = 1


class ClassroomAdmin(admin.ModelAdmin):
    search_fields = ['name']
    inlines = [StudentInClassroomInline]
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
admin.site.register(Homework)
admin.register(Courses)