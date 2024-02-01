from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Person,ElevatorCall,Elevator,Movement
from .serializers import PersonSerializer,ElevatorCallSerializer,ElevatorSerializer,MovementSerializer

class PersonViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.person_data = {'name': 'John Doe', 'age': 30}

    def test_create_person(self):
        response = self.client.post('/elevator_api/person/create_person/', data=self.person_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Person.objects.count(), 1)

    def test_delete_person(self):
        person = Person.objects.create(name='Test Person', age=25)
        response = self.client.delete(f'/elevator_api/person/delete_person/', data={'id': person.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Person.objects.count(), 0)

    def test_delete_nonexistent_person(self):
        response = self.client.delete('/elevator_api/person/delete_person/', data={'id': 999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_person(self):
        person = Person.objects.create(name='Test Person', age=25)
        response = self.client.get('/elevator_api/person/get_person/', data={'id': person.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Person')

    def test_get_nonexistent_person(self):
        response = self.client.get('/elevator_api/person/get_person/', data={'id': 999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_person(self):
        person = Person.objects.create(name='Test Person', age=25)
        updated_data = {'id': person.id, 'name': 'Updated Person', 'age': 30}
        response = self.client.post('/elevator_api/person/update_person/', data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person.refresh_from_db()
        self.assertEqual(person.name, 'Updated Person')

    def test_update_nonexistent_person(self):
        response = self.client.post('/elevator_api/person/update_person/', data={'id': 999, 'name': 'Updated Person'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_people(self):
        Person.objects.create(name='Person 1', age=25)
        Person.objects.create(name='Person 2', age=30)
        response = self.client.get('/elevator_api/person/get_people/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class ElevatorCallViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.elevator = Elevator.objects.create(number_of_floors=10,elevator_speed = 1, current_floor=0)
        self.person = Person.objects.create(name= 'John Doe', age= 30)
        self.call_data = {'elevator': self.elevator.id, 'origin_floor': 3, 'target_floor': 7}

    def test_create_call(self):
        response = self.client.post('/elevator_api/elevator_calls/create_call/', data=self.call_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        #self.assertEqual(ElevatorCall.objects.count(), 1)

    def test_create_call_invalid_target_floor(self):
        self.call_data['target_floor'] = 12  # Set an invalid target floor
        response = self.client.post('/elevator_api/elevator_calls/create_call/', data=self.call_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_call_invalid_origin_floor(self):
        self.call_data['origin_floor'] = -1  # Set an invalid origin floor
        response = self.client.post('/elevator_api/elevator_calls/create_call/', data=self.call_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_call(self):
        call = ElevatorCall.objects.create(elevator=self.elevator, origin_floor=3, target_floor=7,person = self.person)
        response = self.client.get(f'/elevator_api/elevator_calls/get_call/', data={'id': call.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['origin_floor'], 3)

    def test_get_call_not_found(self):
        response = self.client.get('/elevator_api/elevator_calls/get_call/', data={'id': 999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_call(self):
        call = ElevatorCall.objects.create(elevator=self.elevator, origin_floor=3, target_floor=7,person = self.person)
        updated_data = {'id': call.id, 'origin_floor': 5, 'target_floor': 9}
        response = self.client.post('/elevator_api/elevator_calls/update_call/', data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        call.refresh_from_db()
        self.assertEqual(call.origin_floor, 5)

    def test_update_call_not_found(self):
        response = self.client.post('/elevator_api/elevator_calls/update_call/', data={'id': 999, 'origin_floor': 5, 'target_floor': 9}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_call(self):
        call = ElevatorCall.objects.create(elevator=self.elevator, origin_floor=3, target_floor=7,person = self.person)
        response = self.client.delete(f'/elevator_api/elevator_calls/delete_call/', data={'id': call.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ElevatorCall.objects.count(), 0)

    def test_delete_call_not_found(self):
        response = self.client.delete('/elevator_api/elevator_calls/delete_call/', data={'id': 999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_calls(self):
        ElevatorCall.objects.create(elevator=self.elevator, origin_floor=3, target_floor=7,person = self.person)
        ElevatorCall.objects.create(elevator=self.elevator, origin_floor=2, target_floor=5,person = self.person)
        response = self.client.get('/elevator_api/elevator_calls/get_calls/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

class ElevatorViewSetTestCase(TestCase):

    def setUp(self):
        # Create some initial elevators for testing
        self.elevator1 = Elevator.objects.create(number_of_floors=10, elevator_speed=2.0, current_floor=0)
        self.elevator2 = Elevator.objects.create(number_of_floors=15, elevator_speed=1.5, current_floor=0)

    def test_get_elevator(self):

        response = self.client.get('/elevator_api/elevators/get_elevator/', {'id': self.elevator1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.elevator1.id)

    def test_get_elevator_not_found(self):

        response = self.client.get('/elevator_api/elevators/get_elevator/', {'id': 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_elevator(self):

        response = self.client.delete('/elevator_api/elevators/delete_elevator/', {'id': self.elevator1.id})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Elevator.objects.filter(id=self.elevator1.id).exists())

    def test_delete_elevator_not_found(self):

        response = self.client.delete('/elevator_api/elevators/delete_elevator/', {'id': 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_elevator(self):

        data = {'number_of_floors': 12, 'elevator_speed': 2.5, 'current_floor':0}
        response = self.client.post('/elevator_api/elevators/create_elevator/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Elevator.objects.filter(number_of_floors=12, elevator_speed=2.5).exists())

    def test_update_elevator(self):

        data = {'id': self.elevator1.id, 'number_of_floors': 8, 'elevator_speed': 3.0, 'current_floor':0}
        response = self.client.post('/elevator_api/elevators/update_elevator/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_elevator = Elevator.objects.get(id=self.elevator1.id)
        self.assertEqual(updated_elevator.number_of_floors, 8)
        self.assertEqual(updated_elevator.elevator_speed, 3.0)

    def test_update_elevator_not_found(self):
        data = {'id': 9999, 'number_of_floors': 8, 'elevator_speed': 3.0, 'current_floor':0}
        response = self.client.post('/elevator_api/elevators/update_elevator/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_elevators(self):
        response = self.client.get('/elevator_api/elevators/get_elevators/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
