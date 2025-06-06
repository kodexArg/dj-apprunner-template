from django.contrib import admin
from django.urls import path, include
from core.views import home

urlpatterns = [
    path('', home, name='root_home'),
    path('core/', include('core.urls')),
    path('admin/', admin.site.urls),
]
