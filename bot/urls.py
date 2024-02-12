from django.contrib import admin
from django.urls import path
from requests import session
from .views import my_form, chat_session

urlpatterns = [
    path('', my_form, name='chatbot'),
    path('session/', chat_session, name='session'),
    path('session/<str:session_key>/', chat_session, name='chat_history'),
    
]
