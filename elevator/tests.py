from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from datetime import datetime, timedelta
from .models import Person,ElevatorCall,Elevator,Movement
from .serializers import PersonSerializer,ElevatorCallSerializer,ElevatorSerializer,MovementSerializer
import pdb


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
        response = self.client.get(f'/elevator_api/person/get_person/?id={person.id}', format='json')
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
        self.elevator = Elevator.objects.create(number_of_floors=10,elevator_max_speed = 1, current_floor=0)
        self.person = Person.objects.create(name= 'John Doe', age= 30)
        self.call_data = {'elevator': self.elevator.id, 'origin_floor': 3, 'target_floor': 7}

    def test_create_call(self):
        response = self.client.post('/elevator_api/elevator_calls/create_call/', data=self.call_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_call_invalid_target_floor(self):
        self.call_data['target_floor'] = 12
        response = self.client.post('/elevator_api/elevator_calls/create_call/', data=self.call_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_call_invalid_origin_floor(self):
        self.call_data['origin_floor'] = -1
        response = self.client.post('/elevator_api/elevator_calls/create_call/', data=self.call_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_call(self):
        call = ElevatorCall.objects.create(elevator=self.elevator, origin_floor=3, target_floor=7,person = self.person)
        call.save()
        response = self.client.get(f'/elevator_api/elevator_calls/get_call/?id={call.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['origin_floor'], 3)

    def test_get_call_not_found(self):
        response = self.client.get('/elevator_api/elevator_calls/get_call/', data={'id': 999}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_call(self):
        call = ElevatorCall.objects.create(elevator=self.elevator, origin_floor=3, target_floor=7,person = self.person)
        updated_data = {'origin_floor': 5, 'target_floor': 9, 'person': self.person.id, 'elevator': self.elevator.id}
        response = self.client.post(f'/elevator_api/elevator_calls/update_call/?id={call.id}', data=updated_data, format='json')
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
        self.client = APIClient()
        self.elevator1 = Elevator.objects.create(number_of_floors=10, elevator_max_speed=2.0, current_floor=0)
        self.elevator_data = {'number_of_floors':10,'elevator_max_speed':2,'current_floor':0}

    def test_get_elevator(self):
        elevator = Elevator.objects.create(number_of_floors=10, elevator_max_speed=2.0, current_floor=0)
        response = self.client.get(f'/elevator_api/elevator/get_elevator/', {'id': elevator.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], elevator.id)

    def test_get_elevator_not_found(self):

        response = self.client.get('/elevator_api/elevators/get_elevator/', {'id': 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_elevator(self):
        elevator = Elevator.objects.create(number_of_floors=10, elevator_max_speed=2.0, current_floor=0)
        response = self.client.delete(f'/elevator_api/elevator/delete_elevator/', data={'id': elevator.id},format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Elevator.objects.count(),1)

    def test_delete_elevator_not_found(self):

        response = self.client.delete('/elevator_api/elevators/delete_elevator/', {'id': 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_elevator(self):

        response = self.client.post('/elevator_api/elevator/create_elevator/', data = self.elevator_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        ## The self created and the newly created
        self.assertEqual(Elevator.objects.count(),2)

    def test_update_elevator(self):
        elevator = Elevator.objects.create(number_of_floors= 8, elevator_max_speed=3.0, current_floor=0)
        updated_data = {'id': elevator.id, 'number_of_floors': 9, 'elevator_max_speed': 2, 'current_floor':5}
        response = self.client.post('/elevator_api/elevator/update_elevator/', data=updated_data,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        elevator.refresh_from_db()
        self.assertEqual(elevator.number_of_floors, 9)
        self.assertEqual(elevator.elevator_max_speed, 2)

    def test_update_elevator_not_found(self):
        data = {'id': 9999, 'number_of_floors': 8, 'elevator_max_speed': 3.0, 'current_floor':0}
        response = self.client.post('/elevator_api/elevators/update_elevator/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_elevators(self):
        Elevator.objects.create(number_of_floors= 8, elevator_max_speed=3.0, current_floor=0)
        Elevator.objects.create(number_of_floors= 9, elevator_max_speed=5.0, current_floor=1)
        response = self.client.get('/elevator_api/elevator/get_elevators/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #3 because of the sel.elevator1 created
        self.assertEqual(len(response.data), 3)

class MovementViewSetTestCase(TestCase):

    def setUp(self):
        self.elevator = Elevator.objects.create(number_of_floors=10, elevator_max_speed=2.0,current_floor=0)
        self.person = Person.objects.create(name="John Doe", age=30)
        self.elevator_call = ElevatorCall.objects.create(
            origin_floor=2, target_floor=7, elevator=self.elevator, person=self.person
        )
        self.movement1 = Movement.objects.create(
            elevator=self.elevator,
            person=self.person,
            elevator_call=self.elevator_call,
            movement_origin_floor=2,
            movement_final_floor=7,
            call_origin_floor=2,
            call_target_floor=7,
            total_traveled_floors=5,
            total_movement_time_ms=timedelta(minutes=2),
            avg_movement_speed_floor_by_seconds=2,
        )

    def test_get_movement(self):
        response = self.client.get('/elevator_api/movement/get_movement/', {'id': self.movement1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.movement1.id)

    def test_get_movement_not_found(self):

        response = self.client.get('/elevator_api/movement/get_movement/', {'id': 9999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_movement(self):
        movement = Movement.objects.create(
            elevator=self.elevator,
            person=self.person,
            elevator_call=self.elevator_call,
            movement_origin_floor=2,
            movement_final_floor=7,
            call_origin_floor=2,
            call_target_floor=7,
            total_traveled_floors=5,
            total_movement_time_ms=timedelta(minutes=2),
            avg_movement_speed_floor_by_seconds=2,
        )
        response = self.client.delete(f'/elevator_api/movement/delete_movement/?id={movement.id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Movement.objects.count(),1)

    def test_delete_movement_not_found(self):

        response = self.client.delete('/elevator_api/movement/delete_movement/?9999', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_movement(self):

        data = {
            'elevator': self.movement1.elevator.id,
            'person': self.movement1.person.id,
            'elevator_call': self.movement1.elevator_call.id,
            'movement_origin_floor': 3,
            'movement_final_floor': 8,
            'call_origin_floor': 3,
            'call_target_floor': 8,
            'total_traveled_floors': 5,
            'total_movement_time_ms': 120000,  # 2 minutes in milliseconds
            'avg_movement_speed_floor_by_seconds': 2,
        }
        response = self.client.post('/elevator_api/movement/create_movement/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Movement.objects.filter(movement_origin_floor=3, movement_final_floor=8).exists())

    def test_update_movement(self):
        movement = Movement.objects.create(
            elevator=self.elevator,
            person=self.person,
            elevator_call=self.elevator_call,
            movement_origin_floor=2,
            movement_final_floor=7,
            call_origin_floor=2,
            call_target_floor=7,
            total_traveled_floors=5,
            total_movement_time_ms=timedelta(minutes=2),
            avg_movement_speed_floor_by_seconds=2,
        )
        updated_data = {
            'avg_movement_speed_floor_by_seconds': 99,
            'elevator':self.elevator.id,
            'person': self.person.id,
            'elevator_call': self.elevator_call.id
        }
        response = self.client.post(f'/elevator_api/movement/update_movement/?id={movement.id}', data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        movement.refresh_from_db()
        self.assertEqual(movement.avg_movement_speed_floor_by_seconds, 99)

    def test_update_movement_not_found(self):

        data = {'id': 9999, 'movement_origin_floor': 4}
        response = self.client.post('/elevator_api/movement/update_movement/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_movements(self):
        movement1 = Movement.objects.create(
            elevator=self.elevator,
            person=self.person,
            elevator_call=self.elevator_call,
            movement_origin_floor=2,
            movement_final_floor=7,
            call_origin_floor=2,
            call_target_floor=7,
            total_traveled_floors=5,
            total_movement_time_ms=timedelta(minutes=2),
            avg_movement_speed_floor_by_seconds=2,
        )
        movement2 = Movement.objects.create(
            elevator=self.elevator,
            person=self.person,
            elevator_call=self.elevator_call,
            movement_origin_floor=2,
            movement_final_floor=7,
            call_origin_floor=2,
            call_target_floor=7,
            total_traveled_floors=5,
            total_movement_time_ms=timedelta(minutes=2),
            avg_movement_speed_floor_by_seconds=2,
        )
        response = self.client.get('/elevator_api/movement/get_movements/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

