from django.contrib import admin
from .models import CustomUser, Classroom, ParentChildRelationship
# Register your models here.
# admin.site.register(CustomUser)
admin.site.register(Classroom)

class ParentChildInline(admin.TabularInline):
    model = ParentChildRelationship
    fk_name = 'parent'
    extra = 0 
class CustomUserAdmin(admin.ModelAdmin):
    inlines = [ParentChildInline]

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        if obj and obj.user_type == 'parent':
            for inline in self.inlines:
                inline_instance = inline(self.model, self.admin_site)
                inline_instances.append(inline_instance)
        return inline_instances
 
    def get_exclude(self, request, obj=None):
        exclude = super().get_exclude(request, obj) or []
        if obj and obj.user_type != 'student':
            exclude = list(exclude)  # Convert to list to append, get exclude returned a tuple
            exclude.append('matricule')
        return exclude


admin.site.register(CustomUser, CustomUserAdmin)