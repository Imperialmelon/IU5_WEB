from django.shortcuts import render, redirect
from .models import Cargo, Shipping,Shipping_Cargo
from django.core.exceptions import BadRequest

from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Value
from django.db.models import F
from django.db import connection
import psycopg2

USER_ID = 6


def increase(request):

    """
    увеличения числа товара в отправлении
    """
    data = request.POST
    cargo_id = data.get('increase')
    print(cargo_id)
    req = Shipping.objects.filter(client_id=USER_ID,
                                                    status=Shipping.RequestStatus.DRAFT).first()
    shipping_id = req.id
    shipping_cargo = Shipping_Cargo.objects.filter(
        Q(cargo_id=cargo_id) & Q(shipping_id=shipping_id)
    ).first()
    shipping_cargo.amount += 1
    shipping_cargo.save()

    
    return GetShipping(request, shipping_id)


def get_or_create_shipping(user_id):

    """
    создание отправления или создание отправления
    """
    req = Shipping.objects.filter(client_id=USER_ID,
                                                    status=Shipping.RequestStatus.DRAFT).first()
    
    if req is None:
        shipping = Shipping(client_id=USER_ID,status=Shipping.RequestStatus.DRAFT, organization='North Atlantic Treaty Organization')
        shipping.save()
        return shipping.id
    return req.id

def get_cargoes_in_shipping(shipping_id):
     """
     получение числа грузов в текущем черновом отправлении
     """

     print(Shipping_Cargo.objects.filter(shipping_id=shipping_id).select_related('cargo').count())
     return Shipping_Cargo.objects.filter(shipping_id=shipping_id).select_related('cargo').count() 

def GetCargoes_list(cargoes_lists):
    """
    получение страницы услуг
    """
    cargo_name = cargoes_lists.GET.get('cargo_name', '')
    req = Shipping.objects.filter(client_id=USER_ID,
                                                status=Shipping.RequestStatus.DRAFT).first()
    
    
    cargoes_list = Cargo.objects.filter(title__istartswith=cargo_name, is_active=True).order_by('id')
    return render(cargoes_lists, 'cargo_list.html', {'data' : {
        'cargoes' : cargoes_list,
        'cnt' : (get_cargoes_in_shipping(req.id) if req is not None else 0), 'srch_text' : cargo_name,
        'ship_id' : (req.id if req is not None else 0)
    }
    })

def GetCargo(cargo_info, id):
    """
    получение страницы подробнее
    """
    cargo = Cargo.objects.filter(id=id).first()
    return render(cargo_info, 'cargo.html', {'data' : cargo})
        


def add_cargo_to_shipping(request):

    """
    добавление груза в черновое отправление
    """

    data = request.POST
    cargo_id = data.get("add_to_ship")
    shipping_id = get_or_create_shipping(USER_ID)
    shipping_cargo = Shipping_Cargo.objects.filter(
        Q(cargo_id=cargo_id) & Q(shipping_id=shipping_id)
    ).first()
    if not shipping_cargo:
        cargo_shipping = Shipping_Cargo(shipping_id = shipping_id, cargo_id=cargo_id, amount=1)
        cargo_shipping.save()
    return GetCargoes_list(request)



def delete_shipping(request, id):

    """
    удаление отправления
    """

    print(id)

    sql = f"update shipping set status = 'DELETED' where id={id}"
    with connection.cursor() as cursor:
        cursor.execute(sql)

    return GetCargoes_list(request)
    # return GetShipping(request,id)


def get_shipping_data(shipping_id):
    """
    получение содержимого текущей черновой корзины
    """
    req = Shipping.objects.filter(~Q(status=Shipping.RequestStatus.DELETED),
                                                id=shipping_id).first()

    print('shrek')
    
    if req is None:
        raise BadRequest('Invalid Request')
    content = Shipping_Cargo.objects.filter(shipping=shipping_id).select_related('cargo').annotate(cnt=F('amount'), total=F('amount')* F('cargo__price_per_ton')
     ,organization=F('shipping__organization'),        creation_datetime=F('shipping__creation_datetime'))                                                                                      
    org, creation_datetime = content[0].organization, content[0].creation_datetime

    total_sum = 0
    for i in content:

        total_sum+= i.cargo.price_per_ton * i.amount
    return{
        'id' : shipping_id,
        'data' : content,
        'total' : total_sum,
        'org' : org,
        'creation_datetime' : creation_datetime

    }


def GetShipping(cargo_order, id):
    """
    получение страницы текущего чернового отправления
    """
    data = get_shipping_data(id)
    return render(cargo_order, 'ship_list.html', {'data' : data})