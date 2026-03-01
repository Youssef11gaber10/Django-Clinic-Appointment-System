
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # path('__debug__/' , include('debug_toolbar.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('scheduling/', include('scheduling.urls')),
    path('medical/',include('medical.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
