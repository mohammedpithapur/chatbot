from typing import Any, Self
from urllib import response
from django.shortcuts import render,redirect
from django.views import View
from .models import ChatModel
from random_word import RandomWords
import random
from english_words import english_words_set
from django.http import HttpRequest
# Create your views here.
english_words_list = list(english_words_set)
def my_form(request: HttpRequest):
    if request.method == "POST":
        msg = request.POST.get('user-msg')
        if msg:
            print(msg)
            # Save the new message
            message = ChatModel(userinput=msg)
            message.save()

    try:
        # Retrieve the latest chat message where userinput is not null
        latest_message = ChatModel.objects.filter(userinput__isnull=False).order_by('-id').first()
        random_word_list = random.sample(english_words_list, 1)
        
        random_word=random_word_list[0]

        print(request.session)
        print(random_word_list)
        bot=latest_message.userinput + ' ' + random_word
    except ChatModel.DoesNotExist:
        # Handle the case where no matching objects are found
        latest_message = None
        bot = None
    
    return render(request, 'chat.html', {'chats': latest_message,'botreply': bot})
# class UserReplyView(View):
#     def reply(self,request):
#         obj= ChatModel.objects.filter(userinput=12).latest('userinput')
#         return render(request, 'chat.html' ,{'chats':obj})

    