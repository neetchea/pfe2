
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include
from core.views import assign_grades

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include(('core.urls', 'core'), namespace='admin')),

    path('', include('core.urls')),
  
]
