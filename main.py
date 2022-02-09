import requests

def target_search(product_name):
    product_list = []

    if product_name == 'apple':
        product_name = 'apples'

    url = 'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v1'
    payload = {
        'key': 'ff457966e64d5e877fdbad070f276d18ecec4a01',
        'channel': 'WEB',
        'count': '28',
        'default_purchasability_filter': 'true',
        'include_sponsored': 'true',
        'keyword': product_name,
        'offset': '28',
        'page': '/s/'+product_name,
        'platform': 'desktop',
        'pricing_store_id': '3204',
        'scheduled_delivery_store_id': '2229',
        'store_ids': '3204,2229,2300,52,2046',
        'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'visitor_id': '017EB0D0A3240201BE051346B44DDFF7'
    }

    jsonData = requests.get(url, params=payload).json()

    for i in jsonData['data']['search']['products']:
        product_list.append([i['item']['product_description']['title'],i['price']['formatted_current_price']])
    return product_list

def product_choice(product_list):
    product_number = 1
    for i in range(len(product_list)):
        product = product_list[i]
        print(product_number,product[0],product[1])
        product_number += 1
    product_number_choice = int(input('\nChoose a product by entering the number for the product.\nIf the product is not found enter 0\n'))
    if product_number_choice != 0:
        return product_list[product_number_choice-1]

product_list = []

grocery_list = []

while product_list == []:
    product_list = target_search(input('Enter product name:\n'))
    if product_list == []:
        print('Product not found')

grocery_list.append(product_choice(product_list))

print(grocery_list)