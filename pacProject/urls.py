"""pacSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.conf.urls import handler404, handler500
from pacApp import errors


urlpatterns = [
    # this is just what url you will be going to for this
    path('admin/', admin.site.urls),
    path('', include('pacApp.urls')),
    path('pacApp/', include('pacApp.urls')),
    path('accounts/', include('uniauth.urls.cas_only', namespace='uniauth')),
]

handler404 = errors.error_404
handler500 = errors.error_500
