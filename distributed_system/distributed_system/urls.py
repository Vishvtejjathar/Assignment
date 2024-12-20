"""
URL configuration for distributed_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from django.http import HttpResponse
from core.views import insert_data
from django.shortcuts import redirect

# Redirect view for the root path
def redirect_to_insert_data(request):
    return redirect('insert_data')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('insert-data/', insert_data, name='insert_data'),
    path('', redirect_to_insert_data),  # Redirect root to insert-data
]