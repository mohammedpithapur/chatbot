
import imp
from django.shortcuts import render,redirect
from .models import ChatModel
from random import choice
from english_words import english_words_set
from django.http import HttpRequest
import datetime
import json
from django.utils import timezone
from datetime import timedelta
# Create your views here.
english_words_list = list(english_words_set)
def my_form(request: HttpRequest):
    request.session.set_expiry(0)
    msges = None
    if request.method == "POST":
        msg = request.POST.get('user-msg')
        if msg:
            random_word = choice(english_words_list)
            bot = f"{msg} {random_word}"

            
            session_key = request.session.session_key
            chat_data = {
                        "person": msg,
                        "response": bot,
                        'session_key': session_key
                 } 
            objects=ChatModel(chathistory=chat_data,session_key=session_key)
            objects.save()
            msges=ChatModel.objects.filter(chathistory__session_key=session_key)
        else:
                # Handle the case where no matching objects are found
            msges=None
    return render(request, 'chat.html', {'chats': msges})

def chat_session(request: HttpRequest):

    chat_entries = ChatModel.objects.order_by('-time')

    keys_set = set()

    # Categorize keys as "recent" or "old"
    recent_keys = []
    old_keys = []
    for entry in chat_entries:
        # Check if the session key is already in the respective set
        if entry.session_key not in keys_set and entry.time >= (timezone.now() - timedelta(days=2)):
            keys_set.add(entry.session_key)
            recent_keys.append(entry.session_key)
        elif entry.session_key not in keys_set:
            keys_set.add(entry.session_key)
            old_keys.append(entry.session_key)

    context = {
        'recent_keys': recent_keys,
        'old_keys': old_keys,
    }
    print(recent_keys)
    return render(request, 'session.html',{
        'recent_keys': recent_keys,
        'old_keys': old_keys,
        'keys':chat_entries,
    })
def chat_history(request: HttpRequest, session_key):
    if request.method == "GET":
        sessionhistory=ChatModel.objects.filter(session_key=session_key)
    return render(request, 'chathistory.html',{'session':sessionhistory})