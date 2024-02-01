# myapp/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet,ElevatorCallViewSet,MovementViewSet,ElevatorViewSet

router = DefaultRouter()
router.register(r'elevator_calls', ElevatorCallViewSet, basename='elevator_calls')
router.register(r'elevator', ElevatorViewSet, basename='elevator')
router.register(r'movement', MovementViewSet, basename='movement')
router.register(r'person', PersonViewSet, basename='person')

#router.register(r'people', PersonViewSet, basename='person')

urlpatterns = [
    path('', include(router.urls)),
    #path('person/delete_person/<int:pk>/', PersonViewSet.as_view({'delete': 'delete_person'}), name='delete_person'),
]
