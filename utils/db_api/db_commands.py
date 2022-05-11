from typing import List, Coroutine

from asgiref.sync import sync_to_async
from admin_django.usersmanage.models import User, Request

@sync_to_async
def add_user(user_id, full_name, username):
    return User(user_id=int(user_id), name=full_name, username=username).save()

@sync_to_async
def select_all_users():
    return User.objects.all()

@sync_to_async 
def select_user(user_id: int):
    return User.objects.filter(user_id=user_id).first()

# Функция для добаления заявки
@sync_to_async
def add_request(**kwargs):
    res = Request(**kwargs)
    res.save()
    return res.id

# Функция возвращает список активных заявок
@sync_to_async
def get_requests(user_id: int):
    ans = Request.objects.filter(name_user=int(user_id)).all()[:5:-1]
    return ans

# Функция возвращает объект заявки по ее айди
@sync_to_async
def get_status(request_id):
    return Request.objects.filter(id=int(request_id)).first()
