from django.shortcuts import render

from django.http import HttpResponse




cargoes = [
      {'id' : 1, 'title' : 'Техническое оборудование','short_discr' : 'Техническое оборудование для научных объектов' ,'discr' : 'Оборудование спроектировано с учетом самых высоких стандартов и протестировано в условиях, имитирующих марсианскую среду. Подходит для эксплуатации в условиях марсианской среды.',
        'pic' : '1.jpg', 'price' : 15000000, 'formated_price' : "15.000.000"},
       {'id' : 2, 'title' : 'Научное оборудование','short_discr' : 'Различное научное оборудование',     'discr':    'Различное научное оборудование. Предназначено для эксплуатации в условиях научно-исследовательских станций. В состав входят микроскопы, приборы для анализа образцов почвы, астрономическое оборудование и приборы для наблюдения за флорой и фауной с Земли в условиях Марса.', 
 'pic' : '2.jpg', 'price' : 10000000,'formated_price' : "10.000.000"},
        {'id' : 3, 'title' : 'Продовольствие','short_discr' : 'Провиант для сотрудников научных объектов', 'discr' : 'Продовольственные контейнеры, содержащие все необходимые вещества для работников научных станций.'        , 
 'pic' : '3.png','price' : 10000000, 'formated_price' : "10.000.000"},
         {'id' : 4, 'title' : 'Строительные материалы', 'short_discr' : 'Сплавы из нержавеющих металлов, сверхпрочные ткани, композитные стекла ', 'discr' :    'Материалы предназначены для возведения научных и военных баз, имеют возможность эксплуатации в крайне агрессивных средах.'    ,
           'pic' : '4.avif', 'price' : 1000000, 'formated_price' : "10.000.000"},
]

# order = [
#     {'id' : 1, 'items': [
#      {'id' : 1, 'title' : 'Техническое оборудование','cnt' : 2 , 'pic' : 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2xhYjEvJUQxJTgyJUQwJUI1JUQxJTg1JUQwJUJEJUQwJUI4JUQxJTg3LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPTJIMkdYWVRLNUkyRzRESE5XSFFMJTJGMjAyNDA5MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTEyVDE1MjQ1OFomWC1BbXotRXhwaXJlcz00MzIwMCZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSXlTREpIV0ZsVVN6VkpNa2MwUkVoT1YwaFJUQ0lzSW1WNGNDSTZNVGN5TmpFNU5qa3lNQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5jaF9HYUQwNjlxQmhJVXF4d1ZDY2lnbnZQV1U1amhtQmFBVWQ4a1FidjRNZW9MbjZOQTRMenhDVkxWcHFobUU0T2poRGVrcmU0SFlwM1hzdkJKdU9NUSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPTg2YzU4ZWMxLTE5NjctNGFlMi1iMDVhLTA3NWNjYTdjOWQ0MiZYLUFtei1TaWduYXR1cmU9YmRhZDI5OWIzZTZhMTAzYWUwZjcwYWFlZDU0ZGJjOTFmNWM5M2U1YTBiM2E1ZjI1ZTZmOWM3ZTZlMTcyYTQ1ZQ', 'price' : 15000000, 'formated_price' : "15.000.000", 'total' : 30000000},
#              {'id' : 2, 'title' : 'Научное оборудование','cnt' : 3,'pic' : 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2xhYjEvJUQwJUJEJUQwJUIwJUQxJTgzJUQxJTg3JUQwJUJELmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPTJIMkdYWVRLNUkyRzRESE5XSFFMJTJGMjAyNDA5MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTEyVDE1MjUyOVomWC1BbXotRXhwaXJlcz00MzE5OSZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSXlTREpIV0ZsVVN6VkpNa2MwUkVoT1YwaFJUQ0lzSW1WNGNDSTZNVGN5TmpFNU5qa3lNQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5jaF9HYUQwNjlxQmhJVXF4d1ZDY2lnbnZQV1U1amhtQmFBVWQ4a1FidjRNZW9MbjZOQTRMenhDVkxWcHFobUU0T2poRGVrcmU0SFlwM1hzdkJKdU9NUSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPTRlOTdjYzllLTk1YzQtNDUzZi04ZDgyLWFmOWNiYWUxNTk1OSZYLUFtei1TaWduYXR1cmU9MWUwNjgwYWY5MGVhOGIxN2U5OTZiNDk5YzQ5Mzc5MTg1ZmQ3YmM0MTUxZjU4NGYyNTYxYzk1NGI5OTg5ODllNw', 'price' : 10000000,'formated_price' : "10.000.000", 'total' : 30000000}]
#     }, {
#         'id' : 2, 'items' :     {'id' : 1, 'title' : 'Техническое оборудование','cnt' : 2 , 'pic' : 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2xhYjEvJUQxJTgyJUQwJUI1JUQxJTg1JUQwJUJEJUQwJUI4JUQxJTg3LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPTJIMkdYWVRLNUkyRzRESE5XSFFMJTJGMjAyNDA5MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTEyVDE1MjQ1OFomWC1BbXotRXhwaXJlcz00MzIwMCZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSXlTREpIV0ZsVVN6VkpNa2MwUkVoT1YwaFJUQ0lzSW1WNGNDSTZNVGN5TmpFNU5qa3lNQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5jaF9HYUQwNjlxQmhJVXF4d1ZDY2lnbnZQV1U1amhtQmFBVWQ4a1FidjRNZW9MbjZOQTRMenhDVkxWcHFobUU0T2poRGVrcmU0SFlwM1hzdkJKdU9NUSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPTg2YzU4ZWMxLTE5NjctNGFlMi1iMDVhLTA3NWNjYTdjOWQ0MiZYLUFtei1TaWduYXR1cmU9YmRhZDI5OWIzZTZhMTAzYWUwZjcwYWFlZDU0ZGJjOTFmNWM5M2U1YTBiM2E1ZjI1ZTZmOWM3ZTZlMTcyYTQ1ZQ', 'price' : 15000000, 'formated_price' : "15.000.000", 'total' : 30000000},
#     }
# ]

ship = [
    {'id' : 1, 'items': [
     {'id' : 1, 'title' : 'Техническое оборудование','cnt' : 2 , 'pic' : '1.jpg', 'price' : 15000000, 'formated_price' : "15.000.000", 'total' : 30000000},
             {'id' : 2, 'title' : 'Научное оборудование','cnt' : 3,'pic' : '2.jpg', 'price' : 10000000,'formated_price' : "10.000.000", 'total' : 30000000}]
    }, {
        'id' : 2, 'items' :     {'id' : 1, 'title' : 'Техническое оборудование','cnt' : 2 , 'pic' : '1.jpg', 'price' : 15000000, 'formated_price' : "15.000.000", 'total' : 30000000},
    }
]
ORDERS_NUM = len(ship)



def get_list(mas : list, product_name):
    lst_ = []
    print(product_name)
    for product in mas:
        if product['title'].lower().startswith(product_name.lower()):
            lst_.append(product)
            lst_[-1]['path'] = f"http://127.0.0.1:9000/lab1/{lst_[-1]['pic']}"
    return lst_

def get_order_list(ship : list, id):
    ship = ship[id-1]
    mas = []
    for product in ship['items']:
        mas.append(product)
        mas[-1]['path'] = f"http://127.0.0.1:9000/lab1/{mas[-1]['pic']}"
    return mas

# def GetProducts(request):
#     product_name = request.GET.get('product_name', '')
#     # if request.method == 'POST':
#     #     text = request.POST['text'].lower()
#     # else:
#     #     text = ""
#     return render(request, 'products.html', {'data' : {
#         'products' : [product for product in products if product['title'].lower().startswith(product_name)],
#         'cnt' : ORDERS_NUM, 'srch_text' : product_name
#     }
#     })
def GetCargo_list(cargoes_lists):
    product_name = cargoes_lists.GET.get('product_name', '')
    print(product_name)
    # if request.method == 'POST':
    #     text = request.POST['text'].lower()
    # else:
    #     text = ""
    l = get_list(cargoes, product_name)
    return render(cargoes_lists, 'cargo_list.html', {'data' : {
        'products' : l,
        'cnt' : ORDERS_NUM, 'srch_text' : product_name
    }
    })
def GetCargo(cargo_info, id):
    for product in cargoes:
        if product['id'] == id:
            return render(cargo_info, 'cargo.html', {'data' : product})
        

# def GetOrder(request, id):
#     cnt = ORDERS_NUM
#     # cnt = 0
#     if cnt != 0:
#         total = 0
#         for i in order:
#             if i['id'] == id:
#                 for j in i['items']:
#                     total += j['total']
#                 # total += i['pri'][]
#         return render(request, 'order.html',
#                       {'data': {
#                           'order' : order[id-1],
#                           'total' : total
#                       }})
#     return render(request, 'products.html', {'data' : {
#         'products' : [product for product in products if product['title'].lower().startswith("")],
#         'cnt' : ORDERS_NUM
#     }
#     })

def GetCargoes(cargo_order, id):
    cnt = ORDERS_NUM
    # cnt = 0
    if cnt != 0:
        total = 0
        for i in ship:
            if i['id'] == id:
                for j in i['items']:
                    total += j['total']
                # total += i['pri'][]
        mas = get_order_list(ship, id)
        return render(cargo_order, 'ship_list.html',
                      {'data': {
                          'order' : mas,
                          'total' : total
                      }})
    return render(cargo_order, 'cargo_list.html', {'data' : {
        'products' : get_list("", cargoes),
        'cnt' : ORDERS_NUM
    }
    })



