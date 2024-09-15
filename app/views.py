from django.shortcuts import render

from django.http import HttpResponse


products = [
      {'id' : 1, 'title' : 'Техническое оборудование','short_discr' : 'Техническое оборудование для научных объектов' ,'discr' : 'Оборудование спроектировано с учетом самых высоких стандартов и протестировано в условиях, имитирующих марсианскую среду. Подходит для эксплуатации в условиях марсианской среды.',
        'pic' : 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2xhYjEvJUQxJTgyJUQwJUI1JUQxJTg1JUQwJUJEJUQwJUI4JUQxJTg3LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPTJIMkdYWVRLNUkyRzRESE5XSFFMJTJGMjAyNDA5MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTEyVDE1MTI1OFomWC1BbXotRXhwaXJlcz00MzE5OSZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSXlTREpIV0ZsVVN6VkpNa2MwUkVoT1YwaFJUQ0lzSW1WNGNDSTZNVGN5TmpFNU5qa3lNQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5jaF9HYUQwNjlxQmhJVXF4d1ZDY2lnbnZQV1U1amhtQmFBVWQ4a1FidjRNZW9MbjZOQTRMenhDVkxWcHFobUU0T2poRGVrcmU0SFlwM1hzdkJKdU9NUSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPTg2YzU4ZWMxLTE5NjctNGFlMi1iMDVhLTA3NWNjYTdjOWQ0MiZYLUFtei1TaWduYXR1cmU9OTZlYmUyMjkxNGQ2MzJlNzA4MWRhYmE0MmQ0OGY3N2Y4NDNlM2ZmNzA5NDdiZWU2ZThkMTE5ZmVkNmEyMDdlZg', 'price' : 15000000, 'formated_price' : "15.000.000"},
       {'id' : 2, 'title' : 'Научное оборудование','short_discr' : 'Различное научное оборудование',     'discr':    'Различное научное оборудование. Предназначено для эксплуатации в условиях научно-исследовательских станций. В состав входят микроскопы, приборы для анализа образцов почвы, астрономическое оборудование и приборы для наблюдения за флорой и фауной с Земли в условиях Марса.', 
 'pic' : 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2xhYjEvJUQwJUJEJUQwJUIwJUQxJTgzJUQxJTg3JUQwJUJELmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPTJIMkdYWVRLNUkyRzRESE5XSFFMJTJGMjAyNDA5MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTEyVDE1MTgyM1omWC1BbXotRXhwaXJlcz00MzIwMCZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSXlTREpIV0ZsVVN6VkpNa2MwUkVoT1YwaFJUQ0lzSW1WNGNDSTZNVGN5TmpFNU5qa3lNQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5jaF9HYUQwNjlxQmhJVXF4d1ZDY2lnbnZQV1U1amhtQmFBVWQ4a1FidjRNZW9MbjZOQTRMenhDVkxWcHFobUU0T2poRGVrcmU0SFlwM1hzdkJKdU9NUSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPTRlOTdjYzllLTk1YzQtNDUzZi04ZDgyLWFmOWNiYWUxNTk1OSZYLUFtei1TaWduYXR1cmU9MWEwOGY5ZDY1NTdhZmFjNjU5ODU1N2ExMDQ0NjY2ZmNmNzZiZWU3YTNmYTUxMjkzZGM1ODMwZTY5YTUwNjc5Zg', 'price' : 10000000,'formated_price' : "10.000.000"},
        {'id' : 3, 'title' : 'Продовольствие','short_discr' : 'Провиант для сотрудников научных объектов', 'discr' : 'Продовольственные контейнеры, содержащие все необходимые вещества для работников научных станций.'        , 
 'pic' : 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2xhYjEvMTY3NTM4Ljk3MC5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD0ySDJHWFlUSzVJMkc0REhOV0hRTCUyRjIwMjQwOTEyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkxMlQxNTE5NTFaJlgtQW16LUV4cGlyZXM9NDMyMDAmWC1BbXotU2VjdXJpdHktVG9rZW49ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmhZMk5sYzNOTFpYa2lPaUl5U0RKSFdGbFVTelZKTWtjMFJFaE9WMGhSVENJc0ltVjRjQ0k2TVRjeU5qRTVOamt5TUN3aWNHRnlaVzUwSWpvaWJXbHVhVzloWkcxcGJpSjkuY2hfR2FEMDY5cUJoSVVxeHdWQ2NpZ252UFdVNWpobUJhQVVkOGtRYnY0TWVvTG42TkE0THp4Q1ZMVnBxaG1FNE9qaERla3JlNEhZcDNYc3ZCSnVPTVEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnZlcnNpb25JZD02Mjg0YmE4ZS1lZTYwLTQ5NDQtODk3Ny1kODE2ZmFhOTIyMDQmWC1BbXotU2lnbmF0dXJlPTY3MzU4ZmM2MTE3Y2Q4ZDdkNTQ1Y2I1ZDdhN2M2ZWEzMzBmYzg0ZjQ4YjRjZGIwZTRiNjA0ZTY4YzJiNzdkMjc','price' : 10000000, 'formated_price' : "10.000.000"},
         {'id' : 4, 'title' : 'Строительные материалы', 'short_discr' : 'Сплавы из нержавеющих металлов, сверхпрочные ткани, композитные стекла ', 'discr' :    'Материалы предназначены для возведения научных и военных баз, имеют возможность эксплуатации в крайне агрессивных средах.'    ,
           'pic' : 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2xhYjEvJUQxJTgxJUQxJTgyJUQxJTgwJUQwJUJFJUQwJUI4JUQxJTgyLmF2aWY_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD0ySDJHWFlUSzVJMkc0REhOV0hRTCUyRjIwMjQwOTEyJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDkxMlQxNTIyMDBaJlgtQW16LUV4cGlyZXM9NDMyMDAmWC1BbXotU2VjdXJpdHktVG9rZW49ZXlKaGJHY2lPaUpJVXpVeE1pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SmhZMk5sYzNOTFpYa2lPaUl5U0RKSFdGbFVTelZKTWtjMFJFaE9WMGhSVENJc0ltVjRjQ0k2TVRjeU5qRTVOamt5TUN3aWNHRnlaVzUwSWpvaWJXbHVhVzloWkcxcGJpSjkuY2hfR2FEMDY5cUJoSVVxeHdWQ2NpZ252UFdVNWpobUJhQVVkOGtRYnY0TWVvTG42TkE0THp4Q1ZMVnBxaG1FNE9qaERla3JlNEhZcDNYc3ZCSnVPTVEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0JnZlcnNpb25JZD1mNGI3YmM3Mi1hNzJiLTRlZmEtOGU3Zi1hYzI1NjhhOThlNjEmWC1BbXotU2lnbmF0dXJlPWM3MGUwZDFhNWE4MDdkMmVhMzFlN2ZhZGNmYmQxMjE0N2NjNjUzYTZmOWQzNWExMjRhNzExOTFmZGViMzJiYjM', 'price' : 1000000, 'formated_price' : "10.000.000"},
]

order = [
    {'id' : 1, 'items': [
     {'id' : 1, 'title' : 'Техническое оборудование','cnt' : 2 , 'pic' : 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2xhYjEvJUQxJTgyJUQwJUI1JUQxJTg1JUQwJUJEJUQwJUI4JUQxJTg3LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPTJIMkdYWVRLNUkyRzRESE5XSFFMJTJGMjAyNDA5MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTEyVDE1MjQ1OFomWC1BbXotRXhwaXJlcz00MzIwMCZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSXlTREpIV0ZsVVN6VkpNa2MwUkVoT1YwaFJUQ0lzSW1WNGNDSTZNVGN5TmpFNU5qa3lNQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5jaF9HYUQwNjlxQmhJVXF4d1ZDY2lnbnZQV1U1amhtQmFBVWQ4a1FidjRNZW9MbjZOQTRMenhDVkxWcHFobUU0T2poRGVrcmU0SFlwM1hzdkJKdU9NUSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPTg2YzU4ZWMxLTE5NjctNGFlMi1iMDVhLTA3NWNjYTdjOWQ0MiZYLUFtei1TaWduYXR1cmU9YmRhZDI5OWIzZTZhMTAzYWUwZjcwYWFlZDU0ZGJjOTFmNWM5M2U1YTBiM2E1ZjI1ZTZmOWM3ZTZlMTcyYTQ1ZQ', 'price' : 15000000, 'formated_price' : "15.000.000", 'total' : 30000000},
             {'id' : 2, 'title' : 'Научное оборудование','cnt' : 3,'pic' : 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2xhYjEvJUQwJUJEJUQwJUIwJUQxJTgzJUQxJTg3JUQwJUJELmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPTJIMkdYWVRLNUkyRzRESE5XSFFMJTJGMjAyNDA5MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTEyVDE1MjUyOVomWC1BbXotRXhwaXJlcz00MzE5OSZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSXlTREpIV0ZsVVN6VkpNa2MwUkVoT1YwaFJUQ0lzSW1WNGNDSTZNVGN5TmpFNU5qa3lNQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5jaF9HYUQwNjlxQmhJVXF4d1ZDY2lnbnZQV1U1amhtQmFBVWQ4a1FidjRNZW9MbjZOQTRMenhDVkxWcHFobUU0T2poRGVrcmU0SFlwM1hzdkJKdU9NUSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPTRlOTdjYzllLTk1YzQtNDUzZi04ZDgyLWFmOWNiYWUxNTk1OSZYLUFtei1TaWduYXR1cmU9MWUwNjgwYWY5MGVhOGIxN2U5OTZiNDk5YzQ5Mzc5MTg1ZmQ3YmM0MTUxZjU4NGYyNTYxYzk1NGI5OTg5ODllNw', 'price' : 10000000,'formated_price' : "10.000.000", 'total' : 30000000}]
    }, {
        'id' : 2, 'items' :     {'id' : 1, 'title' : 'Техническое оборудование','cnt' : 2 , 'pic' : 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL2xhYjEvJUQxJTgyJUQwJUI1JUQxJTg1JUQwJUJEJUQwJUI4JUQxJTg3LmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPTJIMkdYWVRLNUkyRzRESE5XSFFMJTJGMjAyNDA5MTIlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTEyVDE1MjQ1OFomWC1BbXotRXhwaXJlcz00MzIwMCZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSXlTREpIV0ZsVVN6VkpNa2MwUkVoT1YwaFJUQ0lzSW1WNGNDSTZNVGN5TmpFNU5qa3lNQ3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5jaF9HYUQwNjlxQmhJVXF4d1ZDY2lnbnZQV1U1amhtQmFBVWQ4a1FidjRNZW9MbjZOQTRMenhDVkxWcHFobUU0T2poRGVrcmU0SFlwM1hzdkJKdU9NUSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPTg2YzU4ZWMxLTE5NjctNGFlMi1iMDVhLTA3NWNjYTdjOWQ0MiZYLUFtei1TaWduYXR1cmU9YmRhZDI5OWIzZTZhMTAzYWUwZjcwYWFlZDU0ZGJjOTFmNWM5M2U1YTBiM2E1ZjI1ZTZmOWM3ZTZlMTcyYTQ1ZQ', 'price' : 15000000, 'formated_price' : "15.000.000", 'total' : 30000000},
    }
]
ORDERS_NUM = len(order)
def GetProducts(request):
    if request.method == 'POST':
        text = request.POST['text'].lower()
    else:
        text = ""
    return render(request, 'products.html', {'data' : {
        'products' : [product for product in products if product['title'].lower().startswith(text)],
        'cnt' : ORDERS_NUM, 'srch_text' : text
    }
    })
def GetProoduct(request, id):
    for product in products:
        if product['id'] == id:
            return render(request, 'product.html', {'data' : product})
        

def GetOrder(request, id):
    cnt = ORDERS_NUM
    # cnt = 0
    if cnt != 0:
        total = 0
        for i in order:
            if i['id'] == id:
                for j in i['items']:
                    total += j['total']
                # total += i['pri'][]
        return render(request, 'order.html',
                      {'data': {
                          'order' : order[id-1],
                          'total' : total
                      }})
    return render(request, 'products.html', {'data' : {
        'products' : [product for product in products if product['title'].lower().startswith("")],
        'cnt' : ORDERS_NUM
    }
    })



