from django.shortcuts import render

# Create your views here.
# chat/views.py

from django.shortcuts import render

def chat_page(request):
    return render(request, 'chat.html')
