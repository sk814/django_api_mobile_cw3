# from django.shortcuts import render
import json

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .serializers import VaccineTypeSerializer, VolunteersSerializer
from .models import VaccineType, VolunteersModel
from rest_framework import viewsets, generics, status
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.db import IntegrityError
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.response import Response

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(data['email'], password=data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=201)
        except IntegrityError:
            return JsonResponse({'error':'Email already used! Use another'})


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['email'], password=data['password'])
        # print(user.username)
        if user is None or user.username == "admin":
            return JsonResponse({'error': 'Wrong username/password!'})
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=200)


@csrf_exempt
def adminlogin(request):

    if request.method == 'POST':
        data = JSONParser().parse(request)
        user = authenticate(request, username=data['username'], password=data['password'])
        if user is None or user.username != "admin":
            return JsonResponse({'error': 'Wrong username/password!'})
        else:
            try:
                token = Token.objects.get(user=user)
            except:
                token = Token.objects.create(user=user)
            return JsonResponse({'token':str(token)}, status=200)


class VolunteersViews(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = VolunteersSerializer
    # def post(self, request):
    #     print (request.data)
    #     serializer = VolunteersSerializer(data=request.data)
    #     if serializer.is_valid():
    #         try:
    #             # serializer = serializer.toJSON()
    #             serializer.save()
    #         except Exception as error:
    #             print("Error!!!!!!")
    #             print(error)
    #             return Response(Exception, status=400)
    #
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get_queryset(self):
        return VolunteersModel.objects.all()
    def perform_create(self, serializer):
        serializer.save()

class AllResult(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, format=None):
        try:
            name = VaccineType.objects.values_list('name', flat=True)
            type = VaccineType.objects.values_list('type', flat=True)
            group = VaccineType.objects.values_list('group', flat=True)
            positiveA = VolunteersModel.objects.filter(group='A', positive=True).count()
            positiveB = VolunteersModel.objects.filter(group='B', positive=True).count()
            efficacy_rate = (int(positiveB) - int(positiveA)) / int(positiveB)
            # totalVOl = VolunteersModel.objects.all().count()
            my_dict=[]
            for x in range(len(name)):
                totalPos = VolunteersModel.objects.filter(group=group[x], positive=True).count()
                totalVOl = VolunteersModel.objects.filter(group=group[x]).count()
                print(totalPos)
                print('lets cee')
                print(totalVOl)
                my_dict.append(str({'name': str(name[x]), 'type': str(type[x]), 'vaccineGroup': str(group[x]), 'efficacy_rate': efficacy_rate,
                                    'result': {'volunteer': totalVOl, 'confirm_positive': totalPos}}))
            return  JsonResponse(my_dict, safe=False, status=201)
        except:
            return Http404


        # "group": "A",
        # "dose": 0.5,
        # "positive": false


        # "name": "SLCV2020",
        # "type": "vaccine",
        # "vaccineGroup": "A",
        # "efficacy_rate": "0.9506"
        # "result": {
        #     "volunteer": 100,
        #     "confirm_positive": 1
        # }

#
# class VaccineTypeViewSet(viewsets.ModelViewSet):
#     queryset = VaccineType.objects.all().order_by('name')
#     serializer_class = VaccineTypeSerializer


class FilterView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = VolunteersModel.objects.all()
    serializer_class = VolunteersSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['group', 'dose']


class VacMaker(APIView):
    permission_classes = (IsAuthenticated,)
    @csrf_exempt
    def get(self, request, format=None):
        try:
            totalVOl = VolunteersModel.objects.filter().count()
            totalPositive = VolunteersModel.objects.filter(positive=True).count()
            positive_vaccinated_group = VolunteersModel.objects.filter(group='A', positive=True).count()
            positive_unvaccinated_group = VolunteersModel.objects.filter(group='B', positive=True).count()
            efficacy_rate_all = ((int(totalVOl) - int(totalPositive)) / int(totalVOl)*100)
            positiveHalf = VolunteersModel.objects.filter(dose=0.5, positive=True).count()
            totalVOlHalf = VolunteersModel.objects.filter(dose=0.5,).count()
            positiveFull = VolunteersModel.objects.filter(dose=1, positive=True).count()
            totalVOlFull = VolunteersModel.objects.filter(dose=1,).count()
            efficacy_rate_half_dose = ((int(totalVOlHalf) - int(positiveHalf)) / int(totalVOlHalf)*100)
            efficacy_rate_half_full = ((int(totalVOlFull) - int(positiveFull)) / int(totalVOlFull) * 100)
            return JsonResponse({'totalVolunteer': totalVOl, 'totalPositive': totalPositive, 'positive_vaccinated_group': positive_vaccinated_group,
                                 'positive_unvaccinated_group': positive_unvaccinated_group, 'efficacy_rate_all': efficacy_rate_all,
                                 'efficacy_rate_half_dose': efficacy_rate_half_dose,
                                 'efficacy_rate_half_full': efficacy_rate_half_full}, status=201)

        except:
            return Http404