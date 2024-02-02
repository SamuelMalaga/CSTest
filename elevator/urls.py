# myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from elevator import views
from .views import PersonViewSet,ElevatorCallViewSet,MovementViewSet,ElevatorViewSet

router = DefaultRouter()
router.register(r'elevator_calls', ElevatorCallViewSet, basename='elevator_calls')
router.register(r'elevator', ElevatorViewSet, basename='elevator')
router.register(r'movement', MovementViewSet, basename='movement')
router.register(r'person', PersonViewSet, basename='person')

#router.register(r'people', PersonViewSet, basename='person')

urlpatterns = [
    path('', include(router.urls)),
    # <-----Elevator related urls----->
    #path('elevator_api/person/get_person/', views.PersonViewSet.get_person, name='get_person'),
]
