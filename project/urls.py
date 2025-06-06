from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    # Temporary root redirect - Remove this when main app is defined
    path('', RedirectView.as_view(url='/core/home/', permanent=False)),
    
    path('core/', include('core.urls')),
    path('admin/', admin.site.urls),
]
