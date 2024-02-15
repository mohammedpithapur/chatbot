from django.shortcuts import redirect, render
from requests import delete, session
from .models import ChatModel
from random import choice
from english_words import english_words_set
from django.http import HttpRequest
from django.utils import timezone
from datetime import timedelta
english_words_list = list(english_words_set)
def my_form(request: HttpRequest):
    request.session.set_expiry(300)
    if 'conversations' not in request.session:
        request.session['conversations']=[]
    
    if request.method == "POST":
        msg = request.POST.get('user-msg')
        reset=request.POST.get("reset")
        print(reset)
        if reset:
            print(reset)
            request.session.delete()
            request.session.create()
            
        if msg:
            print(reset)
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
            ChatModel.objects.create(chathistory=chat_data,session_key=session_key)
        
    return render(request, 'chat.html', {'chats': request.session['conversations']})

def chat_session(request, session_key=None):
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

    if session_key is None:
        sessionhistory=None
        return render(request, 'session.html', {
            'recent_keys': recent_keys,
            'old_keys': old_keys,
            'keys': chat_entries,
        })
    else:
         sessionhistory = ChatModel.objects.filter(session_key=session_key)
         print(sessionhistory)
         return render(request, 'session.html',{
            'recent_keys': recent_keys,
            'old_keys': old_keys,
            'keys': chat_entries,
            'sessionhistory':sessionhistory
        })
    
# def resetsession(request: HttpRequest):
    
#     return redirect('chatbot')