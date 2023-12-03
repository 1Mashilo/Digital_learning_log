# ll_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('learning_logs.urls', namespace='learning_logs')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
   
]
