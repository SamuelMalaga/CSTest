from django.contrib.auth.models import Group, User
from elevator.models import Elevator,ElevatorCall,Person,Movement
from elevator.serializers import ElevatorCallSerializer, ElevatorSerializer, PersonSerializer, MovementSerializer
from rest_framework import permissions, viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
import time
from datetime import datetime, timedelta

class ElevatorViewSet(viewsets.ModelViewSet):
  ##Create elevator
  ##Delete elevator
  ##Get Specific elevator
  ##Get all elevators
  queryset = Elevator.objects.all()
  serializer_class = ElevatorSerializer
  @action(detail=False, methods=['get'])
  def get_elevator(self, request, *args, **kwargs):
    try:
        elevator_id = request.data.get('id')
        elevator = Elevator.objects.get(pk=elevator_id)
        serializer = ElevatorSerializer(elevator)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Elevator.DoesNotExist:
        return Response({'error': 'Call not found'}, status=status.HTTP_404_NOT_FOUND)
  @action(detail=False, methods=['delete'])
  def delete_elevator(self, request, *args, **kwargs):
    try:
        elevator_id = request.data.get('id')
        elevator = Elevator.objects.get(pk=elevator_id)
        elevator.delete()
        return Response({'message': 'Elevator deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Elevator.DoesNotExist:
        return Response({'error': 'Elevator not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  @action(detail=False, methods=['post'])
  def create_elevator(self, request, *args, **kwargs):
    return super().create(request, *args, **kwargs)
  @action(detail=False, methods=['post'])
  def update_elevator(self, request, *args, **kwargs):
    try:
        elevator_id = request.data.get('id')
        elevator = Elevator.objects.get(pk=elevator_id)
        serializer = ElevatorSerializer(elevator, data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Elevator.DoesNotExist:
        return Response({'error': 'Elevator not found'}, status=status.HTTP_404_NOT_FOUND)
  @action(detail=False, methods=['get'])
  def get_elevators(self, request, *args, **kwargs):
    try:
        elevator = Elevator.objects.all()
        serializer = ElevatorSerializer(elevator, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Elevator.DoesNotExist:
        return Response({'error': 'Calls not found'}, status=status.HTTP_404_NOT_FOUND)
  @action(detail=False, methods=['post'])
  def call_elevator(self, request, *args, **kwargs):
    elevator_call_id = request.data.get('call_id')
    elevator_call = ElevatorCall.objects.get(pk=elevator_call_id)
    elevator_id = request.data.get('elevator_id')
    elevator = Elevator.objects.get(pk=elevator_id)
    person_id = request.data.get('person_id')
    person = Person.objects.get(pk=person_id)
    movement_starting_floor = elevator.current_floor
    floors_traveled = 0
    movement_start_time = datetime.now()
    if elevator_call.origin_floor > elevator.current_floor:
        print(f"The elevator is below the requested floor {elevator_call.origin_floor}, it is currently in floor {elevator.current_floor}, mooving up to get to the origin floor")
        floors_traveled += self.move_elevator(elevator.current_floor,elevator_call.origin_floor,elevator)
        print(f"The elevator arrived at the requested origin floor {elevator_call.origin_floor}, mooving to the requested floor")
        floors_traveled += self.move_elevator(elevator.current_floor,elevator_call.target_floor,elevator)
        movement_end_time = datetime.now()
        time_delta = movement_end_time -movement_start_time
        #return Response({'Status': f'Finished the elevator movement, floors traveled {floors_traveled} with a time delta of {time_delta}'}, status=status.HTTP_200_OK)
    elif elevator_call.origin_floor < elevator.current_floor:
        print(f"The elevator is above the requested floor {elevator_call.origin_floor}, it is currently in floor {elevator.current_floor}, mooving down to get to the origin floor")
        floors_traveled += self.move_elevator(elevator.current_floor,elevator_call.origin_floor,elevator)
        print(f"The elevator arrived at the requested origin floor {elevator_call.origin_floor}, mooving to the requested floor")
        floors_traveled += self.move_elevator(elevator.current_floor,elevator_call.target_floor,elevator)
        movement_end_time = datetime.now()
        time_delta = movement_end_time -movement_start_time
        #return Response({'Status': f'Finished the elevator movement, floors traveled {floors_traveled} with a time delta of {time_delta}'}, status=status.HTTP_200_OK)
    elif elevator.current_floor == elevator_call.origin_floor:
        print(f"The elevator is already on the requested floor | Floor number {elevator.current_floor}")
        floors_traveled += self.move_elevator(elevator.current_floor,elevator_call.target_floor,elevator)
        movement_end_time = datetime.now()
        time_delta = movement_end_time -movement_start_time
        #return Response({'Status': f'Finished the elevator movement, floors traveled {floors_traveled} with a time delta of {time_delta}'}, status=status.HTTP_200_OK)
    new_movement = Movement.objects.create(
        elevator = elevator,
        person = person,
        elevator_call = elevator_call,
        movement_started_at = movement_start_time,
        movement_finished_at = movement_end_time,
        movement_origin_floor = movement_starting_floor,
        movement_final_floor = elevator_call.target_floor,
        call_origin_floor = elevator_call.origin_floor,
        call_target_floor = elevator_call.target_floor,
        total_traveled_floors = floors_traveled,
        total_movement_time =time_delta,
        avg_movement_speed = 0
    )
    movement_serializer = MovementSerializer(new_movement)
    return Response({'Status': f'Finished the elevator movement, the execution genereted the following movement: {movement_serializer.data}'}, status=status.HTTP_200_OK)
  def move_elevator(self,origin_floor,target_floor,elevator):
    if origin_floor < target_floor:
        ## Moove up
        self.move_up(target_floor,elevator)
        return target_floor - origin_floor
    elif origin_floor > target_floor:
        ## Moove down
        self.move_down(target_floor,elevator)
        return origin_floor-target_floor
  def move_up(self,target_floor,elevator):
    ## Moove up
    floor = elevator.current_floor
    while floor != target_floor:
        print(f"mooving up to floor {target_floor}, currently in floor {floor}")
        time.sleep(elevator.elevator_speed)
        floor +=1
    print(f"arrived at target floor {target_floor}")
    elevator.current_floor = floor
    elevator.save()
    return Response({'Status': 'Arrived at the target floor'}, status=status.HTTP_200_OK)
  def move_down(self,target_floor,elevator):
    floor = elevator.current_floor
    while floor != target_floor:
        print(f"mooving down to floor {target_floor}, currently in floor {floor}")
        time.sleep(elevator.elevator_speed)
        floor -=1
    print(f"arrived at target floor {target_floor}")
    elevator.current_floor = floor
    elevator.save()
    return Response({'Status': 'Arrived at the target floor'}, status=status.HTTP_200_OK)


class ElevatorCallViewSet(viewsets.ModelViewSet):
  queryset = ElevatorCall.objects.all()
  serializer_class = ElevatorCallSerializer
  @action(detail=False, methods=['get'])
  def get_call(self, request, *args, **kwargs):
    try:
        call_id = request.data.get('id')
        call = ElevatorCall.objects.get(pk=call_id)
        serializer = ElevatorCallSerializer(call)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ElevatorCall.DoesNotExist:
        return Response({'error': 'Call not found'}, status=status.HTTP_404_NOT_FOUND)
  @action(detail=False, methods=['delete'])
  def delete_call(self, request, *args, **kwargs):
    try:
        call_id = request.data.get('id')
        call = ElevatorCall.objects.get(pk=call_id)
        call.delete()
        return Response({'message': 'Call deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except ElevatorCall.DoesNotExist:
        return Response({'error': 'Call not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  @action(detail=False, methods=['post'])
  def create_call(self, request, *args, **kwargs):
        elevator_id = request.data.get('elevator')
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            target_floor = request.data.get('target_floor')
            origin_floor = request.data.get('origin_floor')

            if not (0 <= origin_floor <= elevator.number_of_floors and 0 <= target_floor <= elevator.number_of_floors):
                return Response({'Status': 'Origin or target floor is out of bounds'}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ElevatorCallSerializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Elevator.DoesNotExist:
            return Response({'Status': 'Elevator not found'}, status=status.HTTP_404_NOT_FOUND)
  @action(detail=False, methods=['post'])
  def update_call(self, request, *args, **kwargs):
    try:
        call_id = request.data.get('id')
        call = ElevatorCall.objects.get(pk=call_id)
        serializer = ElevatorCallSerializer(call, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ElevatorCall.DoesNotExist:
        return Response({'error': 'ElevatorCall not found'}, status=status.HTTP_404_NOT_FOUND)
  @action(detail=False, methods=['get'])
  def get_calls(self, request, *args, **kwargs):
        calls = ElevatorCall.objects.all()
        serializer = ElevatorCallSerializer(calls, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PersonViewSet(viewsets.ModelViewSet):
  queryset = Person.objects.all()
  serializer_class = PersonSerializer
  """
  ViewSet to CRUD instances of a Person object
  """
  @action(detail=False, methods=['post'])
  def create_person(self, request, *args, **kwargs):
   serializer = PersonSerializer(data=request.data)
   if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
   return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  @action(detail=False, methods=['delete'])
  def delete_person(self, request, *args, **kwargs):
    try:
        person_id = request.data.get('id')  # Assuming you provide the person ID in the request data
        person = Person.objects.get(pk=person_id)
        person.delete()
        return Response({'message': 'Person deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  @action(detail=False, methods=['get'])
  def get_person(self, request, *args, **kwargs):
    try:
        person_id = request.data.get('id')
        person = Person.objects.get(pk=person_id)
        serializer = PersonSerializer(person)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Person.DoesNotExist:
            return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
  @action(detail=False, methods=['post'])
  def update_person(self, request, *args, **kwargs):
    try:
        person_id = request.data.get('id')
        person = Person.objects.get(pk=person_id)
        serializer = PersonSerializer(person, data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found'}, status=status.HTTP_404_NOT_FOUND)
  @action(detail=False, methods=['get'])
  def get_people(self, request, *args, **kwargs):
    people = Person.objects.all()
    serializer = PersonSerializer(people, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

class MovementViewSet(viewsets.ModelViewSet):
  """
  ViewSet to CRUD instances of a Movement object
  """
  queryset = Movement.objects.all()
  serializer_class = MovementSerializer
  @action(detail=False, methods=['get'])
  def get_movement(self, request, *args, **kwargs):
    try:
        movement_id = request.data.get('id')
        movement = Movement.objects.get(pk=movement_id)
        serializer = MovementSerializer(movement)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Movement.DoesNotExist:
        return Response({'error': 'Movement not found'}, status=status.HTTP_404_NOT_FOUND)
  @action(detail=False, methods=['delete'])
  def delete_movement(self, request, *args, **kwargs):
    try:
        movement_id = request.data.get('id')  # Assuming you provide the person ID in the request data
        movement = Movement.objects.get(pk=movement_id)
        movement.delete()
        return Response({'message': 'Movement deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except Movement.DoesNotExist:
        return Response({'error': 'Movement not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  @action(detail=False, methods=['post'])
  def create_movement(self, request, *args, **kwargs):
    return super().create(request, *args, **kwargs)
  @action(detail=False, methods=['post'])
  def update_movement(self, request, *args, **kwargs):
    try:
        movement_id = request.data.get('id')
        movement = Movement.objects.get(pk=movement_id)
        serializer = MovementSerializer(movement, data=request.data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Movement.DoesNotExist:
        return Response({'error': 'Movement not found'}, status=status.HTTP_404_NOT_FOUND)
  @action(detail=False, methods=['get'])
  def get_movements(self, request, *args, **kwargs):
    try:
        movement = Movement.objects.all()
        serializer = MovementSerializer(movement, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Movement.DoesNotExist:
        return Response({'error': 'Movements not found'}, status=status.HTTP_404_NOT_FOUND)


