
from django.contrib import admin
from django.urls import path, include
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include(('core.urls', 'core'), namespace='admin')),

    path('', include('core.urls')),
  
]
