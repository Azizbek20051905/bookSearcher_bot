import requests
import json

BASE_URL = 'http://aziapro.pythonanywhere.com/'

def get_book_search(bookname):
    url = f'{BASE_URL}/booksearch'
    params = {'search': bookname}
    response = requests.get(url=url, params=params).text
    data = json.loads(response)

    return data

def get_books_api():
    url = f'{BASE_URL}/book'
    response = requests.get(url=url).text
    data = json.loads(response)

    return data

def post_books_api(name, file_id, file_type):
    url = f'{BASE_URL}/book'
    response = requests.get(url=url).text
    data = json.loads(response)

    requests.post(url=url, data={"name": name, "file_id": file_id, "file_type": file_type})

    return data

def get_top_books_api():
    url = f'{BASE_URL}/top-book'
    response = requests.get(url=url).text
    data = json.loads(response)

    return data

def get_book_details_api(pk):
    url = f'{BASE_URL}/book/{pk}'
    response = requests.get(url=url).text
    data = json.loads(response)

    return data

def put_book_details_api(pk, number):
    url = f'{BASE_URL}/book/{pk}'
    response = requests.get(url=url).text
    data = json.loads(response)

    requests.put(url=url, data={'likes': number})

    return data

# Update book details api
# def get_book_update_api(pk, types, name):
#     url = f'{BASE_URL}/book/{pk}'
#     response = requests.get(url=url).text
#     data = json.loads(response)

#     data[types] = name

#     requests.put(url=url, data={'name':data['name']})
#     return "Rahmat. Muvaffaqiyatli o'zgartirildi."

def get_chennel_api():
    url = f'{BASE_URL}/channel'
    response = requests.get(url=url).text
    data = json.loads(response)
    
    return data['channel']

def post_chennel_api(name, link):
    url = f'{BASE_URL}/channel'
    response = requests.get(url=url).text
    data = json.loads(response)

    requests.post(url=url, data={"name": name, "link": link})
    
    return data['channel']

def delete_channel_api(pk):
    url = f'{BASE_URL}/channel/{pk}'
    response = requests.get(url=url).text
    data = json.loads(response)

    requests.delete(url=url)
    
    return data

def get_message_api():
    url = f'{BASE_URL}/message'
    response = requests.get(url=url).text
    data = json.loads(response)
    
    return data['message']

def put_message_api(message):
    url = f'{BASE_URL}/message/1'
    response = requests.get(url=url).text
    data = json.loads(response)

    requests.put(url=url, data={'text': message})
    
    return data

def get_mylikes_api(user_id):
    url = f'{BASE_URL}/my-like/user/{user_id}'
    response = requests.get(url=url).text
    data = json.loads(response)

    return data

def post_mylikes_api(user_id, book_id):
    url = f'{BASE_URL}/my-like'
    response = requests.get(url=url).text
    data = json.loads(response)

    requests.post(url=url, data={"telegram_id": user_id, "books": book_id})

    return data['like_book']

def delete_mylikes_api(pk):
    print(pk)
    url = f'{BASE_URL}/my-like/{pk}'
    response = requests.get(url=url).text
    data = json.loads(response)

    requests.delete(url=url)

    return data['like_book']
