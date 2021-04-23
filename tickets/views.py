from django.shortcuts import render
from django.http import JsonResponse
from .models import Guest, Reservation, Movie
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view


#1 without REST and no model query FBV
def no_rest_no_model(request):
    guests = [{
        'id': 1,
        "Name": "Omar",
        "mobile": 789456,
    }, {
        'id': 2,
        'name': "yassin",
        'mobile': 74123,
    }]
    return JsonResponse(guests, safe=False)


#2 model data default djanog without rest


def no_rest_from_model(self):
    guest = Guest.objects.all()

    data = {'guests': list(guest.values('pk', 'name', 'mobile'))}
    return JsonResponse(data)


#3 Function based views
#3.1 GET POST


@api_view(['GET', 'POST'])
def FBV_list(request):

    if request.method == 'GET':
        guest = Guest.objects.all()
        serializer = GuestSerializer(guest, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
