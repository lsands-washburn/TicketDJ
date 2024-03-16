from django.shortcuts import render

# Create your views here.
def ticket_list(request):
    return render(request,'tickets/ticket_list.html')