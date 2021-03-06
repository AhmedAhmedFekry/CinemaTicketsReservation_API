from django.shortcuts import render
from django.http import JsonResponse
from .models import Guest, Reservation, Movie, Post
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer, PostSerializer
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly


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


#3.2 GET PUT DELETE
@api_view(['GET', 'PUT', "DELETE"])
def FBV_pk(request, pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serilizer = GuestSerializer(guest)
        return Response(serilizer.data)
    elif request.method == "PUT":
        serilizer = GuestSerializer(guest, data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data)
        return Response(serilizer.errors, status=status.HTTP_404_NOT_FOUND)
    elif request.method == "DELETE":
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class based view
## list and create == get and post


class CBV_List(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serilizer = GuestSerializer(guests, many=True)
        return Response(serilizer.data)

    def post(self, request):
        serilizer = GuestSerializer(data=request.data)
        if serilizer.is_valid():
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serilizer.data, status=status.HTTP_400_BAD_REQUEST)


#4.2 GET PUT DELETE cloass based views -- pk
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExists:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


## 5 Mixins
########### 5.1 Mixins list
class Mixin_list(mixins.ListModelMixin, mixins.CreateModelMixin,
                 generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


# 5.2 mixins get put delete
class Mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


#6  Generics
#6.1 get and post
class Generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


# authentication_classes = [TokenAuthentication]
#


# 6.2 get put and delete
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


#7 viewsets
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    filter_backend = [filters.SearchFilter]
    search_fields = ['movie']


class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = Reservation


#8 Find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall=request.data['hall'],
        movie=request.data['movie'],
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)


#9 create new reservation
@api_view(['POST'])
def new_reservation(request):

    movie = Movie.objects.get(
        hall=request.data['hall'],
        movie=request.data['movie'],
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)


#10 post author editor
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer