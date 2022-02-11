from tkinter import *
import requests

def target_search(product_name):
    product_list = []

    #Target has a special product page for Apple products
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

def bubble_sort(list):
    for k in range(len(list)):
        for i in range(len(list)-1):
            entry_1 = list[i]
            entry_2 = list[i+1]
            if entry_1[1] > entry_2[1]:
                list[i+1] = list[i]
                list[i] = entry_2
            elif entry_1[1] == entry_2[1]:
                if entry_1[0] > entry_2[0]:
                    list[i + 1] = list[i]
                    list[i] = entry_2
    return list

def search_button_command():
    product = product_name.get()
    if product != '':
        win = Tk()
        win.title('Results')

        product_list = target_search(product)
        product_list = bubble_sort(product_list)

        for i in range(len(product_list)):
            product = product_list[i]
            Label(win, text= product[0]).grid(row=i,column=0)
            Label(win, text=product[1]).grid(row=i, column=1)
            Button(win, text='Add', command=search_button_command).grid(row=i, column=2)

master = Tk()
master.title('Grocery List')
master.geometry("800x600")

Label(master, text = 'Grocery List').grid(row=0,column=0)
Button(master, text='Search For Item', command=search_button_command).grid(row=1,column=1)

product_name = Entry(master)
product_name.grid(row=1,column=0)

mainloop()
