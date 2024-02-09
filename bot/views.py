
from django.shortcuts import render,redirect
from .models import ChatModel
from random import choice
from english_words import english_words_set
from django.http import HttpRequest
import json
# Create your views here.
english_words_list = list(english_words_set)
def my_form(request: HttpRequest):
    request.session.set_expiry(0)
    msg = None
    bot = None
    if request.method == "POST":
        msg = request.POST.get('user-msg')
        if msg:
            random_word = choice(english_words_list)
            bot = f"{msg} {random_word}"

            chat_data = {
                        "person": msg,
                        "response": bot
                 } 
            session_key = request.session.session_key

            objects=ChatModel(chathistory=chat_data,session_key=session_key)
            objects.save()
            
        else:
                # Handle the case where no matching objects are found
            msg = None
            bot = None
    return render(request, 'chat.html', {'chats': msg,'botreply': bot})

def chat_session(request: HttpRequest):

    sessionkey=ChatModel.objects.values("session_key").distinct()
    return render(request, 'session.html',{'session':sessionkey})
def chat_history(request: HttpRequest, session_key):
    if request.method == "GET":
        sessionhistory=ChatModel.objects.filter(session_key=session_key)
        print(sessionhistory)
    return render(request, 'chathistory.html',{'session':sessionhistory})