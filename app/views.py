from django.shortcuts import render, redirect
from .models import Cargo, Shipping,Shipping_Cargo

from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Value
from django.db.models import F
from django.db import connection
import psycopg2

USER_ID = 7

# cargoes = [
#       {'id' : 1, 'title' : 'Техническое оборудование','short_discr' : 'Техническое оборудование для научных объектов' ,'discr' : 'Оборудование спроектировано с учетом самых высоких стандартов и протестировано в условиях, имитирующих марсианскую среду. Подходит для эксплуатации в условиях марсианской среды.',
#         'pic' : '1.jpg', 'price' : 15000000, 'formated_price' : "15.000.000", 'path' : "http://127.0.0.1:9000/lab1/1.jpg"},
#        {'id' : 2, 'title' : 'Научное оборудование','short_discr' : 'Различное научное оборудование',     'discr':    'Различное научное оборудование. Предназначено для эксплуатации в условиях научно-исследовательских станций. В состав входят микроскопы, приборы для анализа образцов почвы, астрономическое оборудование и приборы для наблюдения за флорой и фауной с Земли в условиях Марса.', 
#  'pic' : '2.jpg', 'price' : 10000000,'formated_price' : "10.000.000", 'path' : "http://127.0.0.1:9000/lab1/2.jpg"},
#         {'id' : 3, 'title' : 'Продовольствие','short_discr' : 'Провиант для сотрудников научных объектов', 'discr' : 'Продовольственные контейнеры, содержащие все необходимые вещества для работников научных станций.Продовольственные контейнеры, содержащие все необходимые вещества для работников научных станций'        , 
#  'pic' : '3.png','price' : 10000000, 'formated_price' : "10.000.000", 'path' : "http://127.0.0.1:9000/lab1/3.png"},
#          {'id' : 4, 'title' : 'Строительные материалы', 'short_discr' : 'Сплавы из нержавеющих металлов, сверхпрочные ткани, композитные стекла ', 'discr' :    'Материалы предназначены для возведения научных и военных баз, имеют возможность эксплуатации в крайне агрессивных средах.'    ,
#            'pic' : '4.avif', 'price' : 1000000, 'formated_price' : "10.000.000", 'path' : "http://127.0.0.1:9000/lab1/4.avif"},
# ]



# shippings = [
#     {'id' : 1, 'date' : '12.09.2024','organization' : 'Объединенная Аэрокосмическая Корпорация', 'items': [
#      {'id' : 1, 'title' : 'Техническое оборудование','cnt' : 2 , 'pic' : '1.jpg', 'price' : 15000000, 'formated_price' : "15.000.000", 'total' : 30000000, 'path' : "http://127.0.0.1:9000/lab1/1.jpg"},
#              {'id' : 2, 'title' : 'Научное оборудование','cnt' : 3,'pic' : '2.jpg', 'price' : 10000000,'formated_price' : "10.000.000", 'total' : 30000000, 'path' : "http://127.0.0.1:9000/lab1/2.jpg"}]
#     }, 
#     {
#         'id' : 2, 'date' : '12.09.2024','organization' : 'Объединенная Аэрокосмическая Корпорация', 'items' :     [{'id' : 1, 'title' : 'Техническое оборудование','cnt' : 2 , 'pic' : '1.jpg', 'price' : 15000000, 'formated_price' : "15.000.000", 'total' : 30000000, 'path' : "http://127.0.0.1:9000/lab1/1.jpg"}]
#     }
# ]
# ORDERS_NUM = len(shippings[0]['items'])

def increase(request):
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
    req = Shipping.objects.filter(client_id=USER_ID,
                                                    status=Shipping.RequestStatus.DRAFT).first()
    
    if req is None:
        shipping = Shipping(client_id=USER_ID,status=Shipping.RequestStatus.DRAFT, organization='Объединенная Аэрокосмическая Корпорация')
        shipping.save()
        return shipping.id
    return req.id

def get_cargoes_in_shipping(shipping_id):
     """
     получение числа грузов в текущем черновом отправлении
     """
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
    print(id)

    # req = Shipping.objects.filter(client_id=USER_ID,
    #                                             status=Shipping.RequestStatus.DRAFT).first()
    sql = f"update shipping set status = 'DELETED' where id={id}"
    with connection.cursor() as cursor:
        cursor.execute(sql)
    # data = request.POST
    # id = data.get('drop_shipping')
    return GetShipping(request,id)


def get_shipping_data(shipping_id):
    """
    получение содержимого текущей черновой корзины
    """
    req = Shipping.objects.filter(~Q(status=Shipping.RequestStatus.DELETED),
                                                id=shipping_id).first()
    
    if req is None:
        return {
            'id' : shipping_id,
            'data' : [],
            'total' : 0,
            'org' : '',
            'creation_datetime' : ''
        }
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