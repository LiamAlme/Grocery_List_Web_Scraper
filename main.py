from tkinter import *
import requests
from hashlib import blake2b
import smtplib, ssl
import re
from bs4 import BeautifulSoup


def setup():
    global logged_in
    logged_in = False


def reset():
    global e
    e = blake2b(key=b'DoNotCrackThisKey82394', digest_size=32)


def update_visual_list(product=None,store=None):
    global frame

    if store == 'target':
        target_grocery_list.append(product)
        bubble_sort(target_grocery_list)
    if store == 'cub':
        cub_grocery_list.append(product)
        bubble_sort(cub_grocery_list)

    if len(target_grocery_list)+len(cub_grocery_list) > 1:
        frame.destroy()

    frame = Frame(master)

    if len(target_grocery_list) > 0:
        Label(frame, text='Target').grid(row=3)
        for i in range(len(target_grocery_list)):
            temp = target_grocery_list[i]
            Label(frame, text=temp[0]).grid(row=4+i)
            Label(frame, text='$'+str(temp[1])).grid(row=4+i, column=1)
            Button(frame, text='Remove', command=lambda prod=target_grocery_list[i]: remove(prod,'target')).grid(row=4+i, column=2)
    if len(cub_grocery_list) > 0:
        Label(frame, text='Cub').grid(row=3,column=4)
        for i in range(len(cub_grocery_list)):
            temp = cub_grocery_list[i]
            Label(frame, text=temp[0]).grid(row=4+i,column=4)
            Label(frame, text='$'+str(temp[1])).grid(row=4+i, column=5)
            Button(frame, text='Remove', command=lambda prod=cub_grocery_list[i]: remove(prod,'cub')).grid(row=4+i, column=6)

    frame.grid()


def remove(product,store):
    global frame
    frame.destroy()
    if store == 'target':
        target_grocery_list.remove(product)
    if store == 'cub':
        cub_grocery_list.remove(product)
    update_visual_list()


def target_search(product_name):
    product_list = []

    # Target has a special product page for Apple products
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

    jsondata = requests.get(url, params=payload).json()

    for i in jsondata['data']['search']['products']:
        product_list.append([i['item']['product_description']['title'], i['price']['current_retail']])
    return product_list


def cub_search(product_name):
    url = "https://storefront.cub.com/sm/pickup/rsid/1612/results?q=" + product_name
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    soup = soup.find('div', {'class': 'Listing-sc-vkq6wb kcwlyy'})
    soup = soup.findAll('div')
    product_list = []

    for i in soup:
        prod = str(i.text)
        prod = prod.replace(',', '')
        prod = prod.split()
        name = ''
        price = ''
        for k in prod:
            if '$' not in k:
                name += (k + ' ')
            else:
                price = k
                # Not mine
                price = re.sub('[^\d\.]', '', price)
                name = name[:-1]
                break

        if name != '' and price != '' and 'Buy' not in name:
            temp = list(price)
            temp2 = ''
            for k in range(len(temp)):
                temp2 += temp[k]
                if temp[k] == '.':
                    try:
                        temp2 += temp[k+1]
                        temp2 += temp[k+2]
                        price = temp2
                        if [name, price] not in product_list:
                            product_list.append([name, price])
                    except IndexError:
                        price = price
                        if [name, price] not in product_list:
                            product_list.append([name, price])
    return product_list


def bubble_sort(lst):
    for k in range(len(lst)):
        for i in range(len(lst)-1):
            entry_1 = lst[i]
            entry_2 = lst[i+1]
            if float(entry_1[1]) > float(entry_2[1]):
                lst[i+1] = lst[i]
                lst[i] = entry_2
            elif float(entry_1[1]) == float(entry_2[1]):
                if entry_1[0] > entry_2[0]:
                    lst[i + 1] = lst[i]
                    lst[i] = entry_2
    return lst


def target_search_button_command():
    col = 0
    ro = 0
    product = product_name.get()
    if product != '':
        win = Tk()
        win.title('Results')

        product_list = target_search(product)
        product_list = bubble_sort(product_list)

        for i in range(len(product_list)):
            product = product_list[i]
            if i == len(product_list)//2:
                col = 3
                ro = 0
            Label(win, text=product[0]).grid(row=ro, column=0+col)
            Label(win, text='$'+str(product[1])).grid(row=ro, column=1+col)
            btn = Button(win, text='Add', command=lambda temp=product: update_visual_list(temp,'target'))
            btn.grid(row=ro, column=2+col)
            ro += 1


def cub_search_button_command():
    col = 0
    ro = 0
    product = product_name.get()
    if product != '':
        win = Tk()
        win.title('Results')

        product_list = cub_search(product)
        product_list = bubble_sort(product_list)

        for i in range(len(product_list)):
            product = product_list[i]
            if i == len(product_list)//2:
                col = 3
                ro = 0
            Label(win, text=product[0]).grid(row=ro, column=0+col)
            Label(win, text='$'+str(product[1])).grid(row=ro, column=1+col)
            btn = Button(win, text='Add', command=lambda temp=product: update_visual_list(temp,'cub'))
            btn.grid(row=ro, column=2+col)
            ro += 1


def create_account():
    username = new_username_entry.get()
    password = new_password_entry.get()
    confirm_password = confirm_password_entry.get()
    new_email = email_entry.get()
    flag = False
    if confirm_password == password:
        reset()
        index = 1
        user_list = open('user_list.txt', 'r')
        for line in user_list:
            if str(username+'\n') == line and index % 3 == 1:
                found = Tk()
                found.title('Username Taken')
                found.geometry("500x500")
                Label(found, text='Username is Taken').grid()
                flag = True
            if str(new_email+'\n') == line and index % 3 == 0:
                found = Tk()
                found.title('Email Taken')
                found.geometry("500x500")
                Label(found, text='Email is Taken').grid()
                flag = True
            index += 1
        if not flag:
            user_list.close()
            user_list = open('user_list.txt', 'a')
            user_list.write(username+'\n')
            e.update(password.encode())
            user_list.write(str(e.hexdigest()) + str("\n"))
            user_list.write(new_email + '\n')
            account_created = Tk()
            account_created.title('Account Created')
            account_created.geometry('500x500')
            Label(account_created,text='Account Created').grid()
            ca.destroy()
        user_list.close()


def create_account_window():
    global ca
    ca = Tk()
    ca.title('Create Account')
    ca.geometry("500x500")

    Label(ca, text='Username').grid(row=0, column=0)
    global new_username_entry
    new_username_entry = Entry(ca)
    new_username_entry.grid(row=0, column=1)

    Label(ca, text='Password').grid(row=1, column=0)
    global new_password_entry
    new_password_entry = Entry(ca)
    new_password_entry.grid(row=1, column=1)

    Label(ca, text='Confirm Password').grid(row=2, column=0)
    global confirm_password_entry
    confirm_password_entry = Entry(ca)
    confirm_password_entry.grid(row=2, column=1)

    Label(ca, text='Email').grid(row=3, column=0)
    global email_entry
    email_entry = Entry(ca)
    email_entry.grid(row=3, column=1)

    Button(ca, text='Create Account', command=create_account).grid(row=4, column=0)


def account_login():
    global logged_in
    logged_in = False
    username = username_entry.get()
    password = password_entry.get()
    reset()
    index = 1
    index2 = 1
    flag = 0
    flag2 = 0
    user_list = open("user_list.txt", "r")
    for line in user_list:
        if (str(username) + str("\n")) == str(line):
            if index % 2 == 1:
                flag = 1
                break
        index += 1
    if flag == 1:
        user_list.close()
        user_list = open("user_list.txt", "r")
        e.update(password.encode())
        password = e.hexdigest()
        for line in user_list:
            if (str(password) + str("\n")) == str(line):
                if index + 1 == index2:
                    user_list.close()
                    flag2 = 1
                    break
            if index2 > index + 1:
                user_list.close()
                logged_in = False
                break
            index2 += 1

    if flag2 == 1:
        user_list.close()
        user_list = open("user_list.txt", "r")
        index2 = 1
        for line in user_list:
            if index2 == index+2:
                global email
                email = str(line.rstrip('\n'))
                login.destroy()
                logged_in = True
                user_list.close()
                break
            index2+=1
    else:
        user_list.close()
        failed = Tk()
        failed.title('Login Failed')
        failed.geometry('500x500')
        Label(failed, text='Username or Password is incorrect').grid()
        logged_in = False


def email_grocery_list(sendto):
    smtp_server = "smtp.gmail.com"
    port = 587
    sender_email = "donotreply.grocery.list@gmail.com"
    password = 'vmjqtucoqwuvxqdo'
    message = """\
Subject: Grocery List
"""
    if len(target_grocery_list) >= 1:
        message += 'Target\n'
        for i in range(len(target_grocery_list)):
            prod = target_grocery_list[i]
            message += (str(prod[0])+' $'+str(prod[1])+'\n')

    if len(cub_grocery_list) >= 1:
        message += 'Cub\n'
        for i in range(len(cub_grocery_list)):
            prod = cub_grocery_list[i]
            message += (str(prod[0])+' $'+str(prod[1])+'\n')

    context = ssl.create_default_context()

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sender_email, sendto, message)
    except Exception as e:
        print(e)
    finally:
        server.quit()


setup()

if not logged_in:
    login = Tk()
    login.title('Login')
    login.geometry("500x500")

    Label(login, text='Username').grid(row=0, column=0)
    username_entry = Entry(login)
    username_entry.grid(row=0, column=1)

    Label(login, text='Password').grid(row=1, column=0)
    password_entry = Entry(login)
    password_entry.grid(row=1, column=1)

    Button(login, text='Login', command=account_login).grid(row=2, column=0)
    Button(login, text='Don\'t have an account? Create one', command=create_account_window).grid(row=3, column=0)
    mainloop()

if logged_in:
    master = Tk()
    master.title('Grocery List')
    master.geometry("800x600")

    target_grocery_list = []
    cub_grocery_list = []

    Label(master, text='Grocery List').grid(row=0, column=0)
    Button(master, text='Search Target For Item', command=target_search_button_command).grid(row=1, column=1)
    Button(master, text='Search Cub Foods For Item', command=cub_search_button_command).grid(row=1, column=2)
    Button(master, text='Email List', command=lambda: email_grocery_list(email)).grid(row=1, column=3)

    product_name = Entry(master)
    product_name.grid(row=1, column=0)

    mainloop()