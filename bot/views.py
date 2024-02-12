from django.shortcuts import render,redirect
from .models import ChatModel
from random import choice
from english_words import english_words_set
from django.http import HttpRequest
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.http import HttpResponseRedirect
english_words_list = list(english_words_set)
def my_form(request: HttpRequest):
    if 'conversations' not in request.session:
        request.session['conversations']=[]
    if request.method == "POST":
        msg = request.POST.get('user-msg')
        if msg:
            random_word = choice(english_words_list)
            bot = f"{msg} {random_word}"
            request.session['conversations'].append({'message': msg, 'response': bot})
            request.session.modified = True            
            session_key = request.session.session_key
            chat_data = {
                        "person": msg,
                        "response": bot,
                        'session_key': session_key
                 }           
            objects=ChatModel(chathistory=chat_data,session_key=session_key)
            objects.save()
    return render(request, 'chat.html', {'chats': request.session['conversations']})

def chat_session(request, session_key=None):
    request.session.set_expiry(0)
    chat_entries = ChatModel.objects.order_by('-time')

    keys_set = set()
    recent_keys = []
    old_keys = []
    for entry in chat_entries:
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


    if session_key is None:
        sessionhistory=None
        return render(request, 'session.html', {
            'recent_keys': recent_keys,
            'old_keys': old_keys,
            'keys': chat_entries,
        })
    else:
         sessionhistory = ChatModel.objects.filter(session_key=session_key)
        #  context={per}
         return render(request, 'session.html',{
            'recent_keys': recent_keys,
            'old_keys': old_keys,
            'keys': chat_entries,
            'sessionhistory':sessionhistory
        })