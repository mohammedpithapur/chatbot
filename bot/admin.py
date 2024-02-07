from django.contrib import admin
from .models import ChatModel

@admin.register(ChatModel)
class ChatAdmin(admin.ModelAdmin):
    list_display=['id','userinput','time']
    
