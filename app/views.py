from django.shortcuts import render, redirect
from .models import Cargo, Shipping,Shipping_Cargo
from django.core.exceptions import BadRequest
from django.db.models import Q, F
from django.db import connection
import psycopg2
from lab.settings import MINIO_ENDPOINT_URL, MINIO_ACCESS_KEY,MINIO_BUCKET_NAME,MINIO_SECRET_KEY,MINIO_SECURE
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import *
from .serializers import ShippingSerializer,CargoSerializer,Shipping_CargosSerializer,ResolveShipping, UserSerializer, Shipping_with_info_Serializer,Adding_to_shippingSerializer
from django.core.files.uploadedfile import InMemoryUploadedFile
import os.path
from minio import Minio
from datetime import datetime
from dateutil.parser import parse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token as T
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication


SINGLE_USER = User(id=2, username='OAK')
SINGLE_ADM = User(id=3, username='Admin1')


USER_ID = 6

@api_view(['GET'])
def Get_CargoList(request):
    """
    получение списка услуг
    """
    price_filter = request.query_params.get("min_price")
    filters = None
    if price_filter is not None:
        filters = Q(price_per_ton__gte=price_filter)
    cargo_name = request.query_params.get('cargo_name', '')
    req = Shipping.objects.filter(client_id=SINGLE_USER.id,
                                                status=Shipping.RequestStatus.DRAFT).first()
    if filters is not None:
        cargoes_list = Cargo.objects.filter(filters, title__istartswith=cargo_name, is_active=True).order_by('id')
    else:
         cargoes_list = Cargo.objects.filter(title__istartswith=cargo_name, is_active=True).order_by('id')
    serializer = CargoSerializer(cargoes_list, many=True)

    cnt = Shipping_Cargo.objects.filter(shipping_id=req.id).select_related('cargo').count() if req.id is not None else 0
    
    print(serializer.data)
    # res = {
    #     k : v for 
    # }
    # aboba = manyCargoesSerializer(cargoes_list, many=True)
    cargoes_list = serializer.data
    cargoes_list.append(f'shipping_id : {req.id if req is not None else 0}')
    cargoes_list.append(f'cnt : {cnt}')
    
    return Response(
        cargoes_list,

        status=status.HTTP_200_OK
    )

@api_view(['GET'])
def Get_Cargo(request, pk):
    """
    получение услуги
    """
    cargo = Cargo.objects.filter(id=pk, is_active=True).first()
    if cargo is not None:
        serilizer = CargoSerializer(cargo)
        return Response(serilizer.data, status=status.HTTP_200_OK)
    return Response("No such cargo", status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def add_Cargo(request):
    """
    добавить новую услугу
    """
    serilizer = CargoSerializer(data=request.data)
    if serilizer.is_valid():
        cargo = serilizer.save()
        serilizer = CargoSerializer(cargo)
        return Response(serilizer.data, status=status.HTTP_200_OK)
    return Response('Failed to add cargo', status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def Change_Cargo(request, pk):
    """
    изменить услугу
    """
    cargo = Cargo.objects.filter(id=pk, is_active=True).first()
    if cargo is None:
        return Response('No such cargo', status=status.HTTP_404_NOT_FOUND)
    serializer = CargoSerializer(cargo,data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response('Incorrect data', status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def Delete_Cargo(request, pk):
    """
    удалить услугу
    """
    cargo = Cargo.objects.filter(id=pk, is_active=True).first()
    if cargo is None:
        return Response('No such cargo', status=status.HTTP_404_NOT_FOUND)
    if cargo.logo_file_path != '':
        storage = Minio(endpoint=MINIO_ENDPOINT_URL,access_key=MINIO_ACCESS_KEY,secret_key=MINIO_SECRET_KEY,secure=MINIO_SECURE)
        extension = os.path.splitext(cargo.logo_file_path)[1]
        file = f"{pk}{extension}"
        try:
            print('try')
            storage.remove_object(MINIO_BUCKET_NAME, file)
        except Exception as exception:
            print('except')
            return Response(f'Failed to remove pic due to {exception}', status=status.HTTP_400_BAD_REQUEST)
        cargo.logo_file_path = ""
    cargo.is_active = False
    cargo.save()
    return Response('Succesfully removed the cargo', status=status.HTTP_200_OK)
    
@api_view(['POST'])
def CreateShipping(request, pk):
    """
    создать новое отправление или добавить туда груз
    """
    cargo = Cargo.objects.filter(id=pk, is_active=True)
    if cargo is None:
        return Response('No such cargo', status=status.HTTP_404_NOT_FOUND)
    shipping_id = get_or_create_shipping(SINGLE_USER.id)
    shipping_cargo = Shipping_Cargo.objects.filter(
        Q(cargo_id=pk) & Q(shipping_id=shipping_id)
    ).first()
    if not shipping_cargo:
        cargo_shipping = Shipping_Cargo(shipping_id = shipping_id, cargo_id=pk, amount=1)
        cargo_shipping.save()
    return Response('Succesfully added cargo to shipping')


def get_or_create_shipping(user_id):
    req = Shipping.objects.filter(client_id = SINGLE_USER.id, status=Shipping.RequestStatus.DRAFT).first()
    if req is None:
        shipping = Shipping(client_id = SINGLE_USER.id, status=Shipping.RequestStatus.DRAFT, organization='Объединенная Аэрокосмическая Корпорация')
        shipping.save()
        return shipping.id
    return req.id


@api_view(['POST'])
def load_image_to_minio(request, pk):
    """
    загрузить картинку в минио
    """
    cargo = Cargo.objects.filter(id=pk, is_active=True).first()
    if cargo is None:
        return Response('No such cargo', status=status.HTTP_400_BAD_REQUEST)
    
    storage = Minio(endpoint=MINIO_ENDPOINT_URL,access_key=MINIO_ACCESS_KEY,secret_key=MINIO_SECRET_KEY,secure=MINIO_SECURE)
    extension = os.path.splitext(cargo.logo_file_path)[1]
    file_name = f'{pk}{extension}'
    file = request.FILES.get("image")
    print(file)
    try:
        storage.put_object(MINIO_BUCKET_NAME, file_name, file, file.size)
    except Exception as exception:
        return Response(f'Failed to load pic due to {exception}', status=status.HTTP_400_BAD_REQUEST)
    cargo.logo_file_path = f'http://{MINIO_ENDPOINT_URL}/{MINIO_BUCKET_NAME}/{file_name}'
    cargo.save()
    return Response('Succesfully added/changed pic', status=status.HTTP_200_OK)

@api_view(['GET'])
def get_shippings_list(request):
    """
    получить список отправлений
    """
    status_filter = request.query_params.get("status")
    formation_datetime_start_filter = request.query_params.get("formation_start")
    formation_datetime_end_filter = request.query_params.get("formation_end")
    filters = ~Q(status=Shipping.RequestStatus.DELETED)
    if status_filter is not None:
        filter &= Q(status=status_filter)
    if formation_datetime_start_filter is not None:
        filters &= Q(formation_datetime__gte=parse(formation_datetime_start_filter))
    if formation_datetime_end_filter is not None:
        filters &= Q(formation_datetime__lte=parse(formation_datetime_end_filter))
    shippings = Shipping.objects.filter(filters)
    serializer = ShippingSerializer(shippings, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_shipping(request, pk):
    """
    получить отправление
    """
    filters = Q(id=pk) & ~Q(status=Shipping.RequestStatus.DELETED)
    shipping = Shipping.objects.filter(filters).first()
    if shipping is None:
        return Response('No such shipping', status=status.HTTP_404_NOT_FOUND)
    serializer = Shipping_with_info_Serializer(shipping)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def change_shipping(request, pk):
    """
    изменить отправление
    """
    shipping = Shipping.objects.filter(id=pk).first()
    if shipping is None:
        return Response('No such shipping', status=status.HTTP_404_NOT_FOUND)

    if set(request.data.keys()) != {'organization'}:
        return Response('Can only change `organization` field', status=status.HTTP_400_BAD_REQUEST)  
    serializer = Adding_to_shippingSerializer(shipping, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Incorrect data', status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
def form_shipping(request, pk):
    """
    сформировать отправление
    """
    try:
        shipping = Shipping.objects.filter(id=pk, status=Shipping.RequestStatus.DRAFT).first()
        if shipping is None:
            return Response("INo shipping ready for formation", status=status.HTTP_404_NOT_FOUND)

        if shipping.organization is None or shipping.organization == "":
            return Response("No organization written", status=status.HTTP_400_BAD_REQUEST)


        
        shipping.status = shipping.RequestStatus.FORMED
        shipping.formation_datetime = datetime.now()
        shipping.save()
        serializer = ShippingSerializer(shipping)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)

@api_view(['PUT'])
def resolve_Shipping(request, pk):

    """
    отклонить или завершить оформление
    """
    try:
        shipping = Shipping.objects.filter(id=pk, status=Shipping.RequestStatus.FORMED).first()
        if shipping is None:
            return Response("No siutable shiiping found", status=status.HTTP_404_NOT_FOUND)
        serializer = ResolveShipping(shipping,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            shipping = Shipping.objects.get(id=pk)
            shipping.total_price = calculate_total_sum(shipping.id)
            shipping.completion_datetime = datetime.now()
            shipping.manager = SINGLE_ADM
            shipping.save()
            serializer = ResolveShipping(shipping)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response('Failed to resolve the shipping', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response('Failed to resolve the shipping', status=status.HTTP_400_BAD_REQUEST)


def calculate_total_sum(shipping_id):
        shipping_cargos = Shipping_Cargo.objects.filter(shipping_id=shipping_id)
        total_sum = 0
        for shipping_cargo in shipping_cargos:
            cargo = shipping_cargo.cargo
            amount = shipping_cargo.amount
            total_sum += cargo.price_per_ton * amount
        return total_sum

@api_view(['DELETE'])
def delete_shipping(request, pk):

    """
    удалить оформление
    """
    shipping = Shipping.objects.filter(id=pk,status=Shipping.RequestStatus.DRAFT).first()
    if shipping is None:
        return Response("No such shipping", status=status.HTTP_404_NOT_FOUND)

    shipping.status = Shipping.RequestStatus.DELETED
    shipping.save()
    return Response(status=status.HTTP_200_OK)


# @api_view(['DELETE'])
# def delete_cargo_from_shipping(request, ck, ik):
#     """
#     Удаление груза из отправления
#     """

    
#     cargo_in_shipping = Shipping_Cargo.objects.filter(id=pk).first()
#     if cargo_in_shipping is None:
#         return Response("Cargo not found", status=status.HTTP_404_NOT_FOUND)
#     cargo_in_shipping.delete()
#     shipping_id = cargo_in_shipping.shipping
#     cargo_id = cargo_in_shipping.cargo
#     shipping = Shipping.objects.filter(id=shipping_id).first()
#     cargo = Cargo.objects.filter(id=cargo_id).first()
#     shipping.total_price -= cargo_in_shipping.amount * cargo.price_per_ton
#     shipping.save()
#     return Response(status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_cargo_from_shipping(request, ck, sk):
    """
    Удаление груза из отправления
    """

    
    cargo_in_shipping = Shipping_Cargo.objects.filter(cargo=ck, shipping=sk).first()
    print(ck , sk)
    if cargo_in_shipping is None:
        return Response("Cargo not found", status=status.HTTP_404_NOT_FOUND)
    cargo_in_shipping.delete()
    shipping_id = cargo_in_shipping.shipping
    print(shipping_id)
    cargo_id = cargo_in_shipping.cargo
    shipping = Shipping.objects.filter(id=sk).first()
    cargo = Cargo.objects.filter(id=ck).first()
    shipping.total_price -= cargo_in_shipping.amount * cargo.price_per_ton
    shipping.save()
    return Response(status=status.HTTP_200_OK)


@api_view(['PUT'])
def change_shipping_cargo(request, ck, sk):
    """
    Изменение данных о грузе в отправлении
    """
    print(ck, sk)
    cargo_in_shipping = Shipping_Cargo.objects.filter(cargo=ck, shipping=sk).first()
    if cargo_in_shipping is None:
        return Response("Cargo not found", status=status.HTTP_404_NOT_FOUND)
    serializer = Shipping_CargosSerializer(cargo_in_shipping, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response('Failed to change data', status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_user(request):
    """
    Создание пользователя
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response('Creation failed', status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def login_user(request):
    """
    Вход
    """
    return Response('Login', status=status.HTTP_200_OK)
@api_view(['POST'])
def logout_user(request):

    """
    деавторизация
    """
    return Response('Logout', status=status.HTTP_200_OK)


@api_view(['PUT'])
def update_user(request, pk):
    """
    Обновление данных пользователя
    """
    # user = request.user
    # serializer = UserSerializer(user, data=request.data, partial=True)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    # return Response('Failed to change user data', status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(id=pk).first()
    serializer = UserSerializer(user,data = request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response('Incorrect data', status=status.HTTP_400_BAD_REQUEST)

# def increase(request):

#     """
#     увеличения числа товара в отправлении
#     """
#     data = request.POST
#     cargo_id = data.get('increase')
#     print(cargo_id)
#     req = Shipping.objects.filter(client_id=USER_ID,
#                                                     status=Shipping.RequestStatus.DRAFT).first()
#     shipping_id = req.id
#     shipping_cargo = Shipping_Cargo.objects.filter(
#         Q(cargo_id=cargo_id) & Q(shipping_id=shipping_id)
#     ).first()
#     shipping_cargo.amount += 1
#     shipping_cargo.save()

    
#     return GetShipping(request, shipping_id)


# def get_or_create_shipping(user_id):

#     """
#     создание отправления или создание отправления
#     """
#     req = Shipping.objects.filter(client_id=USER_ID,
#                                                     status=Shipping.RequestStatus.DRAFT).first()
    
#     if req is None:
#         shipping = Shipping(client_id=USER_ID,status=Shipping.RequestStatus.DRAFT, organization='North Atlantic Treaty Organization')
#         shipping.save()
#         return shipping.id
#     return req.id

# def get_cargoes_in_shipping(shipping_id):
#      """
#      получение числа грузов в текущем черновом отправлении
#      """

#      print(Shipping_Cargo.objects.filter(shipping_id=shipping_id).select_related('cargo').count())
#      return Shipping_Cargo.objects.filter(shipping_id=shipping_id).select_related('cargo').count() 

# def GetCargoes_list(cargoes_lists):
#     """
#     получение страницы услуг
#     """
#     cargo_name = cargoes_lists.GET.get('cargo_name', '')
#     req = Shipping.objects.filter(client_id=USER_ID,
#                                                 status=Shipping.RequestStatus.DRAFT).first()
    
    
#     cargoes_list = Cargo.objects.filter(title__istartswith=cargo_name, is_active=True).order_by('id')
#     return render(cargoes_lists, 'cargo_list.html', {'data' : {
#         'cargoes' : cargoes_list,
#         'cnt' : (get_cargoes_in_shipping(req.id) if req is not None else 0), 'srch_text' : cargo_name,
#         'ship_id' : (req.id if req is not None else 0)
#     }
#     })

# def GetCargo(cargo_info, id):
#     """
#     получение страницы подробнее
#     """
#     cargo = Cargo.objects.filter(id=id).first()
#     return render(cargo_info, 'cargo.html', {'data' : cargo})
        


# def add_cargo_to_shipping(request):

#     """
#     добавление груза в черновое отправление
#     """

#     data = request.POST
#     cargo_id = data.get("add_to_ship")
#     shipping_id = get_or_create_shipping(USER_ID)
#     shipping_cargo = Shipping_Cargo.objects.filter(
#         Q(cargo_id=cargo_id) & Q(shipping_id=shipping_id)
#     ).first()
#     if not shipping_cargo:
#         cargo_shipping = Shipping_Cargo(shipping_id = shipping_id, cargo_id=cargo_id, amount=1)
#         cargo_shipping.save()
#     return GetCargoes_list(request)



# def delete_shipping(request, id):

#     """
#     удаление отправления
#     """

#     print(id)

#     sql = f"update shipping set status = 'DELETED' where id={id}"
#     with connection.cursor() as cursor:
#         cursor.execute(sql)

#     return GetCargoes_list(request)
#     # return GetShipping(request,id)


# def get_shipping_data(shipping_id):
#     """
#     получение содержимого текущей черновой корзины
#     """
#     req = Shipping.objects.filter(~Q(status=Shipping.RequestStatus.DELETED),
#                                                 id=shipping_id).first()

#     print('shrek')
    
#     if req is None:
#         raise BadRequest('Invalid Request')
#     content = Shipping_Cargo.objects.filter(shipping=shipping_id).select_related('cargo').annotate(cnt=F('amount'), total=F('amount')* F('cargo__price_per_ton')
#      ,organization=F('shipping__organization'),        creation_datetime=F('shipping__creation_datetime'))                                                                                      
#     org, creation_datetime = content[0].organization, content[0].creation_datetime

#     total_sum = 0
#     for i in content:

#         total_sum+= i.cargo.price_per_ton * i.amount
#     return{
#         'id' : shipping_id,
#         'data' : content,
#         'total' : total_sum,
#         'org' : org,
#         'creation_datetime' : creation_datetime

#     }


# def GetShipping(cargo_order, id):
#     """
#     получение страницы текущего чернового отправления
#     """
#     data = get_shipping_data(id)
#     return render(cargo_order, 'ship_list.html', {'data' : data})