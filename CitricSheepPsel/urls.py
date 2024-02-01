"""
URL configuration for CitricSheepPsel project.

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
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.urls import include, path
from rest_framework import routers
from elevator.admin import admin

from elevator import views

# router = routers.DefaultRouter()
# router.register(r'elevatorCalls', views.ElevatorCallViewSet)
# router.register(r'elevator', views.ElevatorViewSet)
# router.register(r'movement', views.MovementViewSet)
# router.register(r'person', views.PersonViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('elevator_api/',include('elevator.urls'))
]

# urlpatterns += router.urls
