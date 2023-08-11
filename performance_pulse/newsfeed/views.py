from django.shortcuts import render

def news(request):
    return render(request, 'newsfeed/search_news.html')
