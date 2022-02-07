import requests

product_name = input('Enter product name: ')

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
    print(i['item']['product_description']['title'],i['price']['formatted_current_price'])