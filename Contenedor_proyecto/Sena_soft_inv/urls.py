"""
URL configuration for Sena_soft_inv project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# sena_soft_inv/urls.py

from django.contrib import admin
from django.urls import path, include
from aplicacion1.views import index  # Importar la vista index
urlpatterns = [
    path('admin/', admin.site.urls),
    path('aplicacion1/', include('aplicacion1.urls')),
    path('', index, name='index'),  # Ruta para el index
]
