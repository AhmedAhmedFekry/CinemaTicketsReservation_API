"""CinemaTicketsReservation_API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from tickets import views

from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    #1
    path('django/jsonresponsenomodel/', views.no_rest_no_model),
    #2
    path('django/jsonresponsefrommmodel/', views.no_rest_from_model),
    #3.1 GET POST from rest framework function based view @api_view
    path('rest/fbv/', views.FBV_list),
    #3.2 GET PUT DELETE from rest framework function based view @api_view
    path('rest/fbv/<int:pk>', views.FBV_pk),
]
