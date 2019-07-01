"""skill URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from registration.views import create, example_view, login
from django.conf.urls.static import static
from django.conf import settings
from olympiad.views import TaskAPI, TeamAPI, OlympiadAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', create),
    path('hello', example_view),
    path('login', login),
    path('task', TaskAPI.as_view()),
    path('team', TeamAPI.as_view()),
    path('olympiad', OlympiadAPI.as_view()),
    path('api-auth', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)