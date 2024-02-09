from django.contrib import admin
from django.urls import path
from .views import my_form, chat_session, chat_history

urlpatterns = [
    path('', my_form, name='chatbot'),
    path('session/', chat_session, name='session'),
    path('session/<str:session_key>/', chat_history, name='chat_history'),
]
